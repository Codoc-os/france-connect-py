# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/Codoc-os/france-connect-py/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

### Write Documentation

`france-connect-py` could always use more documentation, whether as part of its official docs,
in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/Codoc-os/france-connect-py/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

--- 

## Setting up local environment

Ready to contribute? Here's how to set up `france-connect-py` for local development.

1. Fork the `france-connect-py` repo on GitHub.

2. Clone your fork locally:https://github.com/Codoc-os/france-connect-py/issues.

    * `git clone git@github.com:<your_name_here>/france-connect-py.git`

3. Install your local copy into a virtualenv.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   pip3 install -r requirements_dev.txt
   ```

4. Create a branch for local development:

    * `git checkout -b name-of-your-bugfix-or-feature`

   Now you can make your changes locally.

## Testing your changes

Tests are done using `pytest` and must be written inside the `tests/` directory.

---

### Submitting your changes

1. Ensure your code is correctly formatted and documented:

```sh
./bin/pre_commit.sh
```

2. Commit your changes (you're encouraged to follow the using [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/)) and push your branch to GitHub:

```sh
git add .
git commit -m "<type>: Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

3. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests

2. If the pull request adds functionality, the documentation should be updated.

3. The pull request should work for all [currently supported python version](https://devguide.python.org/versions/).
4. Check https://github.com/qcoumes/france-connect-py/actions and make sure that the tests pass for all supported Python versions.
