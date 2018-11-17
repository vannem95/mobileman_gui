import os
import rospkg
import functools
from python_qt_binding import loadUi
from python_qt_binding.QtCore import Qt, QTimer, Slot
from python_qt_binding.QtGui import QKeySequence
from python_qt_binding.QtWidgets import QShortcut, QWidget
from rqt_gui_py.plugin import Plugin
import subprocess
from std_msgs.msg import Bool
import rospy
from topic_tools.srv import *
from actionlib_msgs.msg import GoalID

class QuickAccessTool(Plugin):

    def __init__(self, context):
        super(QuickAccessTool, self).__init__(context)
        self.setObjectName('QuickAccessTool')
        self._widget = QWidget()
        rp = rospkg.RosPack()
        ui_file = os.path.join(rp.get_path('mobileman_gui'), 'resource', 'QuickAccessTool.ui')
        loadUi(ui_file, self._widget)
        self._widget.setObjectName('QuickAccessToolUI')
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

        # self._populate_vessel_list()

        self._widget.plan_button.pressed.connect(functools.partial(self._on_plan_btn_pressed))
        self._widget.execute_button.pressed.connect(functools.partial(self._on_execute_btn_pressed))
        self._widget.stop_button.pressed.connect(functools.partial(self._on_stop_btn_pressed))

        self._plan_pub = rospy.Publisher('ur5_plan',Bool,queue_size=10)
        self._execute_pub = rospy.Publisher('ur5_execute',Bool,queue_size=10)
        self._stop_pub = rospy.Publisher('ur5_stop',Bool,queue_size=10)

        self._widget.sim_close_button.pressed.connect(functools.partial(self._on_sim_close_btn_pressed))
        self._widget.sim_open_button.pressed.connect(functools.partial(self._on_sim_open_btn_pressed))

        self._sim_gripper_pub = rospy.Publisher('sim_gripper',Bool,queue_size=10)

        self._widget.real_close_button.pressed.connect(functools.partial(self._on_real_close_btn_pressed))
        self._widget.real_open_button.pressed.connect(functools.partial(self._on_real_open_btn_pressed))

        self._real_gripper_pub = rospy.Publisher('gripper_joint',Bool,queue_size=10)

        self._widget.base_stop_button.pressed.connect(functools.partial(self._on_base_stop_btn_pressed))

        self._base_stop_pub = rospy.Publisher('move_base/cancel',GoalID,queue_size=10)


    def _on_plan_btn_pressed(self):

        data1 = Bool()
        data1.data = True
        self._plan_pub.publish(data1)

    def _on_execute_btn_pressed(self):

        data2 = Bool()
        data2.data = True
        self._execute_pub.publish(data2)

    def _on_stop_btn_pressed(self):

        data3 = Bool()
        data3.data = True
        self._stop_pub.publish(data3)

    def _on_sim_close_btn_pressed(self):

        data4 = Bool()
        data4.data = True
        self._sim_gripper_pub.publish(data4)

    def _on_sim_open_btn_pressed(self):

        data5 = Bool()
        data5.data = False
        self._sim_gripper_pub.publish(data5)

    def _on_real_close_btn_pressed(self):

        data6 = Bool()
        data6.data = True
        self._real_gripper_pub.publish(data6)

    def _on_real_open_btn_pressed(self):

        data7 = Bool()
        data7.data = False
        self._real_gripper_pub.publish(data7)

    def _on_base_stop_btn_pressed(self):

        data8 = GoalID()
        data8.id = ""
        self._base_stop_pub.publish(data8)

    def shutdown_plugin(self):
        pass