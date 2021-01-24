from STK_conn import STK_bottom


class panel_stk:
    def __init__(self, ui):
        self.ui = ui

        self.stk_handle = STK_bottom.bottom_stk()
        self.ui.button_startSTK.clicked.connect(lambda: self.stk_handle.start_stk())
        self.ui.button_getSTK.clicked.connect(lambda: self.stk_handle.get_stk())
        self.ui.button_test2.clicked.connect(lambda: self.test_function())
        self.ui.button_executeSTK.clicked.connect(lambda: self.executeButton())

    def test_function(self):
        print(self.stk_handle.simple_connect("Chains_R */Chain/Primary Strands"))

    def executeButton(self):
        text = self.ui.text_STK_comm.toPlainText()

        for p in text.splitlines():
            re_val = self.stk_handle.simple_connect(p)
            print(re_val)


