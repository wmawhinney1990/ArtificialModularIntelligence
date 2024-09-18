""" AMI Core Headspace Blueprint for Markdown """

from flask import redirect, url_for, request

from ami.config import Config
from ami.headspace.blueprint import Blueprint, HeaderButton, route, render_template

from .tool import PerfectYAML

class Utils(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_tempsets(css='utils_styles.css')

    @route('/config_edit/<headspace_name>', methods=['GET', 'POST'])
    def edit_yaml(self, headspace_name: str):
        headspace_dir = Config().get_headspace_dir(headspace_name)

        if headspace_name:
            yaml = PerfectYAML(headspace_dir / "config.yaml")
        else:
            return f"Headspace '{headspace_dir}' not found."

        if request.method == 'POST':
            for key, value in request.form.items():
                yaml.update(key, value)
            yaml.save()

            self.logs.info(f"Config saved for {headspace_name}.")
            return redirect(url_for('Utils.edit_yaml', headspace_name=headspace_name))

        template_settings = self.tempsets.augment(
            heading=f"Config Editor for {headspace_name}",
            buttons=[HeaderButton(form='yaml-editor', value='Save')]
        )

        debug_mode = False
#       if self.logs.level in [ 'DEBUG', 'INFO' ]:
#           debug_mode = True

        yaml_data = yaml.as_items()
        return render_template(
            'config_editor.html',
            tempsets=template_settings,
            data=yaml_data,
            get_comment=yaml.get_comment,
            verbose=debug_mode
        )
