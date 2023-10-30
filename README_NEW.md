# Bojan's project
The software industry evolves continually, demanding fresh and innovative approaches for assessing code quality. Recently, there's been increased interest in using code and project metrics to gauge software quality and security. As the industry expands, developers increasingly rely on extensive open-source code reuse, potentially introducing vulnerabilities.
## Background
The concern stems from inconsistent maintenance of packages, posing security risks in software projects. Notable metrics include:

- The number of lines of code (LoC) of the full project's own code
- The average size of a function/routine in LoC
- The cyclomatic complexity of the main source files
- The number—and seniority—of committers per file
- The cycle time (time between starting and releasing changes in the code)
- Etc.

## Goals
This project primarily focused on seamlessly linking Maven and GitHub packages while computing software metrics. Its key achievement lies in successfully resolving these dual challenges. Connecting GAVs from Maven to GitHub can be complex due to repository maintenance inconsistencies, often leading to irregular repositories requiring ad hoc solutions. By addressing metric computation complexities and optimizing the process, our software provides accurate project metric insights. This dual commitment to linking Maven and GitHub packages and optimizing software metrics underscores its significance and impact in the technical domain for future work.
Our project centers around the manipulation and analysis of software packages in the context of a novel GAV (Group, Artifact, Version)  format. The core objectives of this project are as follows:
- **Input Processing:** We take in software packages in the GAV format, 
allowing for easy identification and retrieval of packages from 
repositories.
- **Repository Linkage:** Our project establishes a connection between the GAV packages on Maven platform and their respective repositories  GitHub platform.
- **Software Metrics:** We employ a range of software metrics to quantify and assess the quality, complexity, and maintainability of the code within these packages.

## Execution Flow
The application is executed through a command-line interface, and goes through a set of well-defined steps to be followed from its initiation until it concludes. These steps are crucial for accurately examining the specified package, and the minimum requirement is the Group Artifact Version (GAV) parameter, specifying the group ID, artifact ID, and version. Key steps are:

1. Parameter Parsing and Environment Configuration
2. Downloading Source Files (from Maven Repository)
3. Extracting Java Files
4. Code Analysis
5. Version Comparison and GitHub integration
6. GitHub Analysis
7. Data Summarizing

# Installation
The installation is very straight forward and requires no specific effort.
### Clone repository
It is very easy to clone the repository with
```python
    git clone https://github.com/bogALT/mvn.git
```
Then lets `cd` in the directory just downloaded. From now on we can start working.
# Examples
I will provide two illustrative examples to demonstrate the performance of the software. One of these examples showcase efficient execution, while the second example exposes an error, highlighting a scenario where the software encounters an issue.
## Example of execution that terminates successfully
The first example I will show is the package com.clever-cloud:biscuit-java:2.2.1.

### How to
The application is autonomous, just start it and will do everything automatically: In the terminal we type: 
```python
    python3 main.py -slimit 0.1 -gav com.clever-cloud:biscuit-java:2.2.1
```
From now on the execution will be automatic:
Output: 
```console
    Starting the program for GAV =  com.clever-cloud:biscuit-java:2.2.1
    Slimit the program for GAV =  0.1

    download url =  https://repo1.maven.org/maven2/com/clever-cloud/biscuit-java/2.2.1/biscuit-java-2.2.1-sources.jar
    download url =  https://repo1.maven.org/maven2/com/clever-cloud/biscuit-java/2.2.1/biscuit-java-2.2.1.pom
    Archive:  pom_jar/biscuit-java-2.2.1-sources.jar
    
       creating: packages/biscuit-java-2.2.1-sources/META-INF/
       inflating: packages/biscuit-java-2.2.1-sources/META-INF/MANIFEST.MF  
       creating: packages/biscuit-java-2.2.1-sources/com/
       creating: packages/biscuit-java-2.2.1-sources/com/clevercloud/
       creating: packages/biscuit-java-2.2.1-sources/com/clevercloud/biscuit/
       creating: packages/biscuit-java-2.2.1-sources/com/clevercloud/biscuit/error/
       creating: packages/biscuit-java-2.2.1-sources/com/clevercloud/biscuit/crypto/
       creating: packages/biscuit-java-2.2.1-sources/com/clevercloud/biscuit/datalog/
       creating: packages/biscuit-java-2.2.1-sources/com/clevercloud/biscuit/datalog/expressions/
                  [...]
                  
    Analyzed files = 47, Exceptions = 0
    On average we have 29.92 locs per method
    
    Starting Cyclomatic complexity analysis
    AVG CCN per file = 96.96. 
    
    Searching for version precedent to  2.2.1
    Searching among 4 pages. This may take more than 4 seconds according to your internet speed and maven central server status.
    Pages left = 4
    ||||
    
    I retrieved the following possible urls from the XML file:  ['https://github.com/clevercloud/biscuit-java']
    GH manager created -------------------
    Adding ['https://github.com/clevercloud/biscuit-java'] to the GM object
    
    Git Repo manager created --------------
    
    https://github.com/clevercloud/biscuit-java looks to be a valid gh repo url. Returning!
    Trying to clone repo with url = https://github.com/clevercloud/biscuit-java
    Comparing: Current version = 2.2.1 and Precedent version 2.2.0

    GAV                            |  com.clever-cloud : biscuit-java : 2.2.1
    AVG Cyclomatic Complexity      | 96.96
    AVG LOCs per method            | 29.92
    Precedent version              | 2.2.0
    Code Churn                     | 5
    GitHub Nr. changed files       | 4
    GitHub Nr. commits             | 5
```
## Example of execution that terminates with an error
Let's analyze here an example of execution that does not get until the end. In this case, we are unable to match Maven's repository and GitHub repository because we did not find any github link in the POM file on Maven's repository.

In the terminal we type: 
```python
    python3 main.py -slimit 0.1 -gav com.mitchellbosecke:pebble:2.4.0
```
From now on the execution will be automatic:
Output: 
```console
        Starting the program for GAV =  com.mitchellbosecke:pebble:2.4.0
    Slimit the program for GAV =  0.1
    
    --------------------------------------------------------------------------------
    JAR Extractor created
    Directory packages/pebble-2.4.0-sources already exists. Skipping extraction of pom_jar/pebble-2.4.0-sources.jar.
    
    --------------------------------------------------------------------------------
             Current file =  packages/pebble-2.4.0
    
    -sources/com/mitchellbosecke/pebble/PebbleEngine.java (Size = 0.017 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/lexer/Syntax.java (Size = 0.009 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/lexer/TokenStream.java (Size = 0.004 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/lexer/TemplateSource.java (Size = 0.006 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/lexer/LexerImpl.java (Size = 0.019 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/lexer/Token.java (Size = 0.002 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/lexer/Lexer.java (Size = 0.001 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/operator/Associativity.java (Size = 0.0 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/operator/UnaryOperator.java (Size = 0.001 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/operator/BinaryOperatorImpl.java (Size = 0.001 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/operator/BinaryOperator.java (Size = 0.001 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/operator/UnaryOperatorImpl.java (Size = 0.001 MB, Limit = 0.1 MB)
         Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/TestInvoc
    
        ationExpression.java (Size = 0.002 MB, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/TextNode.java (Size = 0.001 MB, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/ImportNode.java (Size = 0.001 MB, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/FlushNode.java (Size = 0.001 MB, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/BodyNode.java (Size = 0.002 MB, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/IfNode.java (Size = 0.003 M

    B, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/ParallelNode.java (Size = 0.003 MB, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/RootNode.java (Size = 0.001 MB, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/CacheNode.java (Size = 0.004 MB, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/SetNode.java (Size = 0.001 MB, Limit = 0.1 MB)
             Current file =  packages/pebble-2.4.0-sources/com/mitchellbosecke/pebble/node/IncludeNode.java (Size = 0.002 MB, Limit = 0.1 MB)
        
    On average we have 16.68 locs per method
    
    
    --------------------------------------------------------------------------------
    
    Starting Cyclomatic complexity analysis
    Init cyclomatic complexity analyzer
    AVG CCN per file = 8.49. For more detailed output uncomment code in CyclomaticComplexityAnalyzer.py::start()
    
    --------------------------------------------------------------------------------
    Searching for version precedent to  2.4.0
    Searching among 4 pages. This may take more than 4 seconds according to your 

    internet speed and maven central server status.
        Pages left = 4
        ||||Version 2.4.0 has predecessor 2.3.0
        
        
    I retrieved the following possible urls from the XML file:  ['http://github.com/mbosecke/pebble.git']
        GH manager created -------------------
        Adding ['http://github.com/mbosecke/pebble.git'] to the GM object


        --------- E N D E D   W I T H    E R R O R ---------
    
        Error Message thet raised the Exception:
        I did not find any valid Github url in the POM file!
```
As you can see we have a "half-report" which contains only a subset of metrics.
Consider that this is only one of the errors that may occur. For example:
1. The GAV passed as input is not present on Maven's repository, 
2. Not every version is present on Maven and GitHub repository
3. And so on

## Where are the outputs
The outputs are in `JSON` format in the folder `data`


## License

[MIT](https://choosealicense.com/licenses/mit/)
