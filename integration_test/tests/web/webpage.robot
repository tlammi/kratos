*** Settings ***
Documentation  Web page tests

Library  KratosLib
Library  SeleniumLibrary


Test Setup  Do Setup
Test Teardown  Do Teardown

Force Tags  WEB_PAGE

*** Test Cases ***
Test Open
    Open Browser  localhost:8080  chrome
    Maximize Browser Window
    Set Selenium Speed  0
    Title Should Be  kratos

*** Keywords ***

Do Setup
    Start kratos web server

Do Teardown
    Kill all kratos processes
    Close Browser