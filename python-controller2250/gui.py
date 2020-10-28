# Imports
import wx, wx.adv
from os import path

from config import *
from logger import logger



# Class: RackApp
class RackApp(wx.App):
    # Init
    def __init__(self, serial):
        logger.info('Initializing RackApp')

        self.serial = serial

        super(RackApp, self).__init__()

    
    # Event: Start
    def on_start(self, event=None):
        logger.info('Starting...')

        self.taskbar_icon.set_icon('tray_y.png')

        # Serial connection
        self.serial.open()

        if self.serial.is_open:
            # Start timer
            logger.info('Serial port opened, starting timer')
            self.timer.Start(REFRESH_RATE)
            self.taskbar_icon.set_icon('tray.png')
        else:
            logger.error('Could not open serial port (all attempts exhausted)')
            self.on_stop()


    # Event: Stop
    def on_stop(self, event=None):
        logger.info('Stopping...')

        self.timer.Stop()

        if self.serial.is_open:
            logger.info('Closing serial connection..')
            self.serial.close()

        self.taskbar_icon.set_icon('tray_r.png')


    # Event: Quit
    def on_quit(self, event):
        logger.info('Quitting application...')

        # self.stop()
        self.taskbar_icon.RemoveIcon()
        self.taskbar_icon.Destroy()
        self.frame.Destroy()


    # Event: Init
    def OnInit(self):     
        # Instance checker
        self.name = '%s-%s' % ('RackApp', wx.GetUserId())
        self.instance = wx.SingleInstanceChecker(self.name)

        # Check instance
        if self.instance.IsAnotherRunning():
            dlg = wxh.InfoMessage('RackApp is already running', 'RackApp')
            dlg.Centre() 
            dlg.ShowModal()
            dlg.Destroy() 
            return False

        # Create frame and taskbar icon
        self.frame = wx.Frame()
        self.taskbar_icon = TaskBarIcon(self.frame)

        self.SetTopWindow(self.frame)#RackFrame(self))

        # Power events
        self.Bind(wx.EVT_POWER_SUSPENDED, self.OnSystemSuspend)
        self.Bind(wx.EVT_POWER_RESUME, self.OnSystemResume)

        # Timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
    
        self.on_start()

        return True


    # Event: System suspend
    def OnSystemSuspend(self, e):
        logger.warning('System is about to suspend')
        if self.timer.IsRunning():
            self.on_stop()


    # Event: System resume
    def OnSystemResume(self, e):
        logger.warning('System returning from suspended state')
        if not self.timer.IsRunning():
            self.on_start()

    
    # Event: Exit
    def OnExit(self):
        logger.info('Bye!')
        return super(RackApp, self).OnExit()


    # Event: Timer
    def OnTimer(self, event):
        # Process serial data
        success = self.serial.process()

        if not success:
            # Stop timer
            self.on_stop()
       


# Class: TaskBarIcon
class TaskBarIcon(wx.adv.TaskBarIcon):
    # Init
    def __init__(self, frame):
        # Super
        super(TaskBarIcon, self).__init__()

        # App
        self.app = wx.GetApp()

        # Icon
        self.set_icon('tray_r.png')
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_clicked)


    def on_left_clicked(self, event):
        logger.info('Left clicked on taskbar icon')
        if self.app.timer.IsRunning():
            self.app.on_stop()
        else:
            self.app.on_start()

        # self.app.on_stop if self.app.timer.IsRunning() else self.app.on_start
        # dlg = wx.TextEntryDialog(self.frame, 'message')
        # dlg.ShowModal()
        # result = dlg.GetValue()
        # dlg.Destroy()
        # if result:
        #     self.frame.parent.string_data = result
        #     self.frame.parent.string_delay = 10


    # Create popup menu
    def CreatePopupMenu(self):
        menu = wx.Menu()

        # Header
        menu.Append(self.create_menu_item(menu, APP_NAME, **{
            # 'icon': 'ico_calendar.png', 
            'bold': True,
            'enable': False
        }))

        menu.AppendSeparator()

        if self.app.serial.sensor_data:
            # Stats
            menu.Append(self.create_menu_item(menu, **{
                'label': 'CPU (temp)\t%d°C' % (self.app.serial.sensor_data[0]),
                'icon': 'processor_temp.png', 
            }))
            menu.Append(self.create_menu_item(menu, **{
                'label': 'CPU (load)\t%d %%' % (self.app.serial.sensor_data[1]),
                'icon': 'processor.png', 
            }))

            menu.Append(self.create_menu_item(menu, **{
                'label': 'GPU (temp)\t%d°C' % (self.app.serial.sensor_data[2]),
                'icon': 'processor_temp.png', 
            }))
            menu.Append(self.create_menu_item(menu, **{
                'label': 'GPU (load)\t%d %%' % (self.app.serial.sensor_data[3]),
                'icon': 'processor.png', 
            }))

            menu.AppendSeparator()

        # Connect/Disconnect
        menu.Append(self.create_menu_item(menu, **{
            'label': 'Disconnect' if self.app.timer.IsRunning() else 'Connect',
            # 'icon': 'book.png', 
            'bind': self.app.on_stop if self.app.timer.IsRunning() else self.app.on_start,
            'enable': True,
        }))

        # Close
        menu.Append(self.create_menu_item(menu, 'Quit', **{
            # 'icon': 'book.png', 
            'bind': self.app.on_quit,
            'enable': True,
        }))
        
        return menu


    # Set icon
    def set_icon(self, name):
        self.SetIcon(wx.Icon(wx.Bitmap(self.get_resource(name))), APP_NAME)


    # Set bold
    def create_menu_item(self, menu, label, icon=None, bind=None, bold=False, color=None, enable=True):
        item = wx.MenuItem(menu, wx.ID_ANY, label)
        if icon:
            item.SetBitmap(wx.Bitmap(self.get_resource(icon)))
        if bind:
            menu.Bind(wx.EVT_MENU, bind, id=item.GetId())
        if color:
            item.SetTextColour(wx.Colour(color))
        font = item.GetFont() 
        if bold:
            font.SetWeight(wx.BOLD) 
        # font.SetFamily(wx.MODERN)
        # font.SetPointSize(20)
        # font.SetPixelSize((10, 10))
        font.SetFaceName('Consolas')
        item.SetFont(font)
        item.Enable(enable)

        return item


    # Get resource
    def get_resource(self, file_name):
        '''
        try:
            base_path = sys._MEIPASS # PyInstaller creates a temp folder and stores path in _MEIPASS
        except Exception:
        '''
        # base_path = path.join(path.dirname(__file__))
        # base_path = path.abspath(path.dirname(__name__))
        # base_path = BASE_DIR
        resource = path.join(BASE_DIR, 'resources', file_name)
        return resource