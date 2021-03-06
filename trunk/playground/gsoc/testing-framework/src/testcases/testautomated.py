#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

from clcolorize import colorize


class TestAutomated(object):
    """This class will perform an automated test, the purpose of which is to run
    a command, get its output and compare it with the expected output, which is
    already encoded in the testcase file."""
    def __init__(self, package, element, summary=None, report=None):
        self.package = package
        self.element = element
        self.summary = list()
        self.report = list()

    def test_automated_main(self):
        """Entry point for the testcase type automated."""
        case = self.element.xpath('case')
        totalCases = len(case)
        counter = 0
        print ''
        while counter < totalCases:
            print 'Case {0} of {1}'.format(counter+1, totalCases),
            self.report.append('')
            self.report.append('Case {0} of {1}'.format(counter+1, totalCases))
            for text in case[counter].iter('text'):
                print colorize(text.text, 'bold')
            commandList = []
            for command in case[counter].iter('command'):
                commandList.append(command.text)
            totalCommands = len(commandList)
            self.report.append('Total Commands: {0}'.format(totalCommands))
            self.report.append('-')
            commandCounter = 0
            while commandCounter < totalCommands:
                self.report.append('Command {0}: {1}'.format(commandCounter+1,
                                                    commandList[commandCounter]))
                try:
                    runCommand = subprocess.Popen(commandList[commandCounter].split(),
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE)
                except OSError:
                    self.report.append('Output: Invalid command or invalid option')
                    commandCounter += 1 
                    continue
                output, error = runCommand.communicate()
                if error:
                    self.report.append('Error: {0}'.format(error.rstrip()))
                    commandCounter += 1 
                    continue
                self.report.append('Output: {0}'.format(output.rstrip()))
                commandCounter += 1
            for expected in case[counter].iter('expected'):
                self.report.append('Expected: {0}'.format(expected.text))
                if expected.text in output:
                    self.summary.append('Success')
                else:
                    self.summary.append('Failed')
            print '... Done'
            counter += 1