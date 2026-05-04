# Problem to solve

The blog engine uses multiple configuration settings directly in the code. It impacts the extensibility of the engine for other blogs.

We need to put the configuration in `config/config.yml`. The YAML file should contain the configuration of the blog as defined in the beginning of `src/build.py` file.

The configuration file should be as clear as possible with sections as below:

- General configuration (as described in the `src/build.py`: SITE_TITLE, SITE_URL, POSTS_DIR, BUILD_DIR)
- Languages (as described in the `src/build.py`:LANGUAGES, READING_TIME_LABELS, BACK_LABELS)
- Publish (as described in the `src/build.py`:DEFAULT_TIMEZONE, DEFAULT_PUBLISH_HOUR)
- Theme (as described in the `src/build.py`:THEME_DIR, TEMPLATE_FILE, STYLE_FILE)

The configuration file must be extensively documented.

The configuration file is read and managed by a specific Python source file (not in the `build.py`) to avoid having a big Python source code.

All configuration items are mandatory. When the YAML file is read, the configuration manager must check that all the configuration items are set properly (aka present). For the labels, the configuration manager checks that all `LANGUAGES` are properly set in the `READING_TIME_LABELS` and `BACK_LABELS`. If there is a missing property, the configuration must return the error on the console in an intelligible way to provide context and a way to fix it for the user.

By default the configuration is read from `config/config.yml` but the configuration file can be passed to the `build` command if necessary.
