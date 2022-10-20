import os

import wx
import wx.adv
import wx.lib.newevent as NE
from wxasync import WxAsyncApp, StartCoroutine
import asyncio
import subprocess
import time
import logging

from player import Player
from config import get_footswitch_keys, get_footswitch_device

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('PEDALIER')

CONFIG_DIR = os.path.expanduser("~/.config/rdt")
CONFIG_FILE = os.path.join(CONFIG_DIR, 'rdt.ini')

footswitch_event, EVT_FOOTSWITCH = NE.NewEvent()
config_pedal_event, EVT_CFG_PEDAL = NE.NewEvent()

# Pedals code
left_k, center_k, right_k = get_footswitch_keys()
pedal = {left_k: 'Left',
         center_k: 'Centre',
         right_k: 'Right'}

ID_VLC_BTN = wx.NewIdRef()
ID_CONNECT_VLC_BTN = wx.NewIdRef()

# Messages
VLC_READY_MSG = "VLC is ready..."
VLC_NOT_READY_MSG = "VLC is not ready"


class ConfigDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.InitUI()
        self.SetSize(350, 450)
        self.SetTitle("Configuration")
        self.Bind(EVT_FOOTSWITCH, self.footswitch_setup_callback)

    def InitUI(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(pnl, -1,
                           label="Pour configurer votre pédalier, il suffit "
                                 "de cliquer sur les boutons suivants "
                                 "puis de presser la pédale correspondante.",
                           style=wx.TE_MULTILINE|wx.ALIGN_CENTER, size=(200, 50))
        vbox.Add(st, flag=wx.ALL|wx.EXPAND, border=10)

        hbox_1 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(pnl, label='Pédale de gauche', size=(160, 50))
        self.lst = wx.StaticText(pnl, label='...')
        hbox_1.Add(btn, 1, flag=wx.LEFT|wx.TOP, border=5)
        hbox_1.Add(self.lst, flag=wx.LEFT|wx.TOP, border=30)
        vbox.Add(hbox_1)

        hbox_2 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(pnl, label='Pédale du milieu', size=(160, 50))
        self.cst = wx.StaticText(pnl, label='...')
        hbox_2.Add(btn, 1, flag=wx.LEFT|wx.TOP, border=5)
        hbox_2.Add(self.cst, flag=wx.LEFT|wx.TOP, border=30)
        vbox.Add(hbox_2)

        hbox_3 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(pnl, label='Pédale de droite', size=(160, 50))
        self.rst = wx.StaticText(pnl, label='...')
        hbox_3.Add(btn, 1, flag=wx.LEFT|wx.TOP, border=5)
        hbox_3.Add(self.rst, flag=wx.LEFT|wx.TOP|wx.EXPAND, border=30)
        vbox.Add(hbox_3, flag=wx.LEFT)

        pnl.SetSizer(vbox)

    def footswitch_setup_callback(self, evt):
        print(evt.code)
        print('renard')

    def OnClose(self, e):
        self.Destroy()


class FootswitchMonitor(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title,
                         size=(350, 150))
        self.makeMenuBar()
        self.CreateStatusBar()
        StartCoroutine(self.footswitch_callback, self)
        self.Bind(EVT_FOOTSWITCH, self.OnFootswitchEvent)
        self.connect_vlc()
        self.InitUI()
        self.active = True

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        toolMenu = wx.Menu()
        configItem = toolMenu.Append(-1, "Configurer le pédalier")
        connectVLCItem = toolMenu.Append(-1, "Connecter VLC",
                                         "Cela nécessite que VLC soit en marche")

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(toolMenu, "&Tools")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnSetupFootswitch, configItem)
        self.Bind(wx.EVT_MENU, self.OnConnectVLC, connectVLCItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        vlc_btn = wx.Button(panel, label="Start VLC", id=ID_VLC_BTN)
        hbox1.Add(vlc_btn, 1, flag=wx.LEFT|wx.EXPAND, border=10)
        self.Bind(wx.EVT_BUTTON, self.OnPanelButton, id=ID_VLC_BTN)
        vbox.Add(hbox1, flag=wx.ALIGN_CENTER|wx.RIGHT|wx.TOP, border=10)
        panel.SetSizer(vbox)

    def OnExit(self, event):
        self.Close(True)

    def OnPanelButton(self, evt):
        id = evt.GetId()
        if id==ID_VLC_BTN:
            # start VLC Player
            try:
                self.player = Player()
            except:
                subprocess.Popen(['vlc'])
                time.sleep(1)
                self.connect_vlc()

    def OnAbout(self, event):
        description = "This is a RDT pedal tool to control VLC Player" \
                      "About Footswitch Monitor"
        info = wx.adv.AboutDialogInfo()
        info.SetIcon(wx.Icon('assets/rdt_pedalier.svg', wx.BITMAP_TYPE_PNG))
        info.SetName('Footswitch Monitor')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetWebSite('https://rd-transcription.fr')
        info.AddDeveloper('Bastien Roques')
        wx.adv.AboutBox(info)

    def OnSetupFootswitch(self, event):
        device = get_footswitch_device()
        if device:
            cDialog = ConfigDialog(None)
            cDialog.ShowModal()
            cDialog.Destroy()
        else:
            wx.MessageBox("Je n'ai pas trouvé de pédalier. Est-il branché ?",
                          "Configuration du pédalier",
                          wx.OK|wx.ICON_ERROR)

    def OnConnectVLC(self, evt):
        if not self.connect_vlc():
            wx.MessageBox('Erreur de connection à VLC', VLC_NOT_READY_MSG,
                          wx.OK|wx.ICON_ERROR)

    def connect_vlc(self):
        try:
            self.player = Player()
            self.SetStatusText(VLC_READY_MSG)
            return True
        except:
            self.player = None
            self.SetStatusText(VLC_NOT_READY_MSG)

    def OnFootswitchEvent(self, event):
        try:
            if event.code == left_k:
                self.player.rewind()
            elif event.code == center_k:
                self.player.play_pause()
            elif event.code == right_k:
                self.player.forward()
        except Exception:
            self.connect_vlc()

    def SetStatusFootPressed(self, event):
        status_text = self.GetStatusBar().StatusText.split(' /')[0]
        if event.value == 1:
            self.SetStatusText(status_text + ' /' + pedal[event.code])
        elif event.value == 0:
            self.SetStatusText(status_text)

    async def footswitch_callback(self):
        """
        type: 1 (keycode)
        value:
            0 = key_up
            1 = key_down
            2 = key_hold
        code: code of the key (eg. 48 for left)
        """
        device = get_footswitch_device()
        device.grab()
        while self.active:
            async for ev in device.async_read_loop():
                if ev.type == 1:
                    logger.debug(f"Key code: {ev.code} key value (up, down, hold): {ev.value}")
                    self.SetStatusFootPressed(ev)
                    if ev.value == 1 and ev.code == center_k:
                        # we don't want the signal sent twice or more in
                        # case of playpause command, so we create the event
                        # only when key is pressed.
                        event = footswitch_event(code=ev.code)
                        wx.PostEvent(self, event)
                    elif ev.code in (left_k, right_k):
                        # left & right foot can receive multiple signals.
                        # It means that while the pedal is hold, the signal
                        # continue which allow to back or forward longer.
                        event = footswitch_event(code=ev.code)
                        wx.PostEvent(self, event)


async def main_async():
    app = WxAsyncApp()
    monitor = FootswitchMonitor(None, title='Pedal Monitoring')
    monitor.Show()
    app.SetTopWindow(monitor)
    await app.MainLoop()


if __name__ == '__main__':
    asyncio.run(main_async())
