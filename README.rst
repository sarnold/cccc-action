A Github Action for cccc
========================

|social_blob|

|ci|

|sec| |pre|

|tag| |license|

What is cccc?
=============

cccc_ is a program to analyze C++, C, and Java source code and report on
some useful software metrics. By default, cccc will look for the standard
source file extensions for all supported languages (currently Java, C++,
and C) starting in the repository root.  You can override the default
extensions or specifiy a list of source directories if needed (see below).

The output report is a directory with both ``.html`` and ``.xml`` files,
plus an options file containing all options used for that run, and a
small database file with the analysis data.

In order to do something with the output, you can choose one (or both)
of the following two options:

1. Commit the output dirrectory to your repo, either to the current branch
   or another one (eg, a gh-pages branch). This option is *disabled* by
   default.
2. Upload the output as an artifact (see the basic example below).

Usage
=====

Create a .yml file under .github/workflows with the following contents.

Default configuration
---------------------

::

    name: cccc
    on: [push]

    jobs:
      check:
        name: cccc-action
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2

          - name: cccc action step
            uses: sarnold/cccc-action@main
            with:
              github_token: ${{ secrets.GITHUB_TOKEN }}

          - name: upload metrics report
            uses: actions/upload-artifact@v2
            with:
              name: metrics
              path: ./metrics


Advanced configuration
----------------------

::

    name: cccc
    on: [push]

    jobs:
      check:
        name: cccc-action
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
            with:
              fetch-depth: 0

          - name: cccc action step
            uses: sarnold/cccc-action@main
            with:
              github_token: ${{ secrets.GITHUB_TOKEN }}
              commit_report: true
              target_branch: gh-pages
              source_dirs: |
                src
              file_extensions: |
                .h
                .cc


Input Options
-------------

.. note:: All input options are optional *except* ``github_token``. By
          default, the ``commit_report`` option uses ``--dry-run`` so
          you can see what it *would* do before you actually enable it,
          however, you need to set ``target_branch`` (without ``commit_report``)
          to see the output from ``--dry-run``. Note you must also
          **create the empty target branch** and push it to your repo first.


:github_token: GITHUB_TOKEN secret (automatically provided by Github,
  you don't need to set this up)
:commit_report: Whether to commit the report files (default: false)
:output_dir: Directory name for report (default: "metrics")
:source_dirs: Directory names to search for source files (default: repository root)
  Type is multiline string.
:target_branch: Branch that the action will target (default: None)
:language: Set the target language if needed (one of 'c++', 'c', or 'java')
:file_extensions: File extensions to search for (default uses built-in list).
  Type is multiline string.


Input Constraints
-----------------

* **target_branch** will not create a new branch (you must create and
  push the branch *before* enabling this option)
* **language** does not limit the search for source files (use this option
  if any source files are mis-detected)
* use **source_dirs** and/or **file_extensions** to narrow the source file
  search as needed
* **source_dirs** should be the relative path from the repository root,
  ie, use something like `src/java` if the source directories are nested


Please refer to the cccc_ doumentation for further details.


.. _cccc: https://sarnold.github.io/cccc/


Operating System Support
------------------------

This action runs in a Docker container and requires the Ubuntu_ CI runner.
In your workflow job configuration, you'll need to set the ``runs-on``
property to ``ubuntu-latest``::

    jobs:
      metrics:
        runs-on: ubuntu-latest

The ``cccc`` tool itself is built and tested in github CI using Linux,
Macos, and Windows, so you can always generate output on your local
machine as needed.


.. _Ubuntu: https://ubuntu.com/

.. |social_blob| image:: https://socialify.git.ci/sarnold/cccc-action/image?description=1&font=Raleway&issues=1&language=1&owner=1&pulls=1&stargazers=1&theme=Light
    :alt: cccc-action

.. |ci| image:: https://github.com/sarnold/cccc-action/actions/workflows/main.yml/badge.svg
    :target: https://github.com/sarnold/cccc-action/actions/workflows/main.yml
    :alt: CI test status

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. |sec| image:: https://img.shields.io/badge/Security-Bandit-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/PyCQA/bandit
    :alt: Scanned by Bandit

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/cccc-action?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/cccc-action/releases
    :alt: GitHub tag

.. |license| image:: https://img.shields.io/github/license/sarnold/cccc-action
    :target: https://github.com/sarnold/cccc-action/blob/main/LICENSE
    :alt: License
