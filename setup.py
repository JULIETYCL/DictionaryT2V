from cx_Freeze import setup, Executable

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", None, None, "This is a description", "IconId", None),
    ],
    "Icon": [
        ("IconId", "icon.ico"),
    ],
}

build_exe_options = {
    'include_files' : [
        'web'
    ],
    'include_msvcr': True
}

bdist_msi_options = {
    "add_to_path": True,
    "data": msi_data,
    "upgrade_code": "{a6e6f846-9df3-4815-8e3c-9d65acf87c97}",
    "install_icon": "icon.ico",
    "summary_data": {
        "comments" : "",
        "keywords": "Education AI Learning"
    }
}

executables = [
    Executable(
        'app.py',
        base = 'console',
        target_name = 'Dictionary.ai',
        icon = 'icon',
        shortcut_name = "Dictionary.ai",
        shortcut_dir = "StartMenuFolder"
    )
]

setup(name='Dictionary.ai',
      version = '1.0',
      description = 'Dictionary.ai desktop app',
      options = {
          'build_exe': build_exe_options,
          'bdist_msi': bdist_msi_options
      },
      executables = executables)
