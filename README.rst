A Github Action for cccc
========================

**what is cccc?**

cccc_ is a program to analyze C++, C, and Java source code and report on
some useful software metrics. By default, cccc will look for the standard
source file extensions for all supported languages (currently Java, C++,
and C) starting in the repository root.  You can override the default
extensions or specifiy a top-level source directory if needed (see below).

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
            uses: sarnold/cccc-action@master
            with:
              github_token: ${{ secrets.GITHUB_TOKEN}}

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

          - name: cccc action step
            uses: sarnold/cccc-action@master
            with:
              github_token: ${{ secrets.GITHUB_TOKEN}}
              source_dir: 'cccc'  # source dir for main cccc sources
              commit_report: 'true'
              target_branch: 'gh-pages'
              file_extensions: |
                '.h'
                '.cc'


Input Options
-------------

.. note:: All input options are optional *except* ``github_token``. By
          default, the ``commit_report`` option uses ``--dry-run`` so
          you can see what it *would* do before you actually enable it.


:github_token: GITHUB_TOKEN secret (automatically provided by Github,
  you don't need to set this up)
:commit_report: Whether to commit the report files (default: false)
:output_dir: Directory name for report (default: "metrics")
:source_dir: Directory name to search for source files (default is repository root)
:target_branch: Branch that the action will target (default is current branch)
:language: Set the target language if needed (one of 'c++', 'c', or 'java')
:file_extensions: File extensions to search for (default uses built-in list).
  Type is multiline string.


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


.. _: https://ubuntu.com/
