from tethys_sdk.base import TethysAppBase, url_map_maker


class ReferenceTimeseriesJsonCompiler(TethysAppBase):
    """
    Tethys app class for Reference Timeseries JSON Compiler.
    """

    name = 'Reference Timeseries JSON Compiler'
    index = 'refts_json_compiler:home'
    icon = 'refts_json_compiler/images/icon.gif'
    package = 'refts_json_compiler'
    root_url = 'refts-json-compiler'
    color = '#1abc9c'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        url_map = url_map_maker(self.root_url)

        url_maps = (url_map(name='home',
                            url='refts-json-compiler',
                            controller='refts_json_compiler.controllers.home'),
                    url_map(name='ajax_convert_files',
                            url='refts-json-compiler/convert-files',
                            controller='refts_json_compiler.controllers_ajax.ajax_convert_files')
                    )

        return url_maps
