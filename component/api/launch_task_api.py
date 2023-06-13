from common.bytecontext import *
from common.byterunner import ByteRunner
from common.decorators import component


class LaunchTaskAPI(ByteRunner):

    @component("launch_manage/launch_task/search_live_templates.json")
    def search_live_templates(self, context: ByteContext):
        self.execute(context)