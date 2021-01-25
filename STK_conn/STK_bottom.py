from comtypes.client import CreateObject, GetActiveObject


class bottom_stk:
    root = None

    def start_stk(self):
        try:
            uiApp = CreateObject('STK11.Application')
            uiApp.Visible = True
            uiApp.UserControl = True

            self.root = uiApp.Personality2
            # self.root.NewScenario("test_scenario")

        except Exception as e:
            print(e)

    def get_stk(self):
        try:
            uiApp = GetActiveObject('STK11.Application')

            self.root = uiApp.Personality2

        except Exception as e:
            print(e)

    def simple_connect(self, comm):
        val = ""
        try:
            re_val = self.root.ExecuteCommand(comm)
            for p in range(re_val.Count):
                val += re_val.item(p)
        except Exception as e:
            print(e)

        return val


if __name__ == "__main__":
    test = bottom_stk()
    test.start_stk()
    test.simple_connect("New / */Satellite ERS2")
