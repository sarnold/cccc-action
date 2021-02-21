

**what is cccc?**

cccc is a program to analyse C++, C, and Java source code and report on
some useful software metrics.

Usage
=====

Create a .yml file under .github/workflows with the following contents

Default configuration
---------------------

name: metrics
on: [push]

jobs:
  check:
    name: cccc-action
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
 
      - name: cccc action step
        uses: ./ # Uses an action in the root directory
        with:
          github_token: ${{ secrets.GITHUB_TOKEN}}
          source_dir: 'src'

      - name: upload report
        uses: actions/upload-artifact@v2
        with:
          name: metrics
          path: ./metrics
