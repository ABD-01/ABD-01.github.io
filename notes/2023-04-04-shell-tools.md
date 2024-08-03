# Shell Tools

```{article-info}
:avatar: https://avatars.githubusercontent.com/u/63636498?v=4
:avatar-link: https://github.com/ABD-01
:avatar-outline: muted
:author: Muhammed Abdullah
:date: April 04, 2023
:read-time: "{sub-ref}`wordcount-minutes` min read"
```

Usefull shell tools such as `sed`, `tr`, `xargs`, `awk`, etc...

## SED

- Append in file

```Shell
sed -i "$ a sometext" somefile.txt
```

- Insert in line

```Shell
sed -i "1 i sometext" somefile.txt
```

- replace

```Shell
sed -n '2 s/regular_expression/\1/p'
		↓   |                       ↓ ↓
 Silent ↓                   Group  Print
      2nd line            Identifier
      address		
```

## Echo

Literal \n

```{admonition} Reference
:class: seealso

Echo newline in Bash prints literal \n  
How do I print a newline?  
[https://stackoverflow.com/questions/8467424/echo-newline-in-bash-prints-literal-n](https://stackoverflow.com/questions/8467424/echo-newline-in-bash-prints-literal-n)  
```


```Shell
echo "Hello\nWorld"
>> Hello\nWorld
echo -e "Hello\nWorld"
>> Hello
>> World
```


## tr

Translate or delete

- delete quotes

```Shell
tr -d '"' 
```

  

- Killing process in Bash

```{admonition} Reference
:class: seealso
What to do when Ctrl + C can't kill a process?  
Ctrl + C doesn't always work to kill the current process (for instance, if that process is busy in certain network operations).  
[https://superuser.com/a/243464](https://superuser.com/a/243464)  
```

 

## xargs

Using `xargs` and `cp`

[bash - How to Properly Use xargs With cp - Stack Overflow](https://stackoverflow.com/questions/72253410/how-to-properly-use-xargs-with-cp)

```Shell
ldd application.exe | sed 's/.*=> //g' | sed -E 's/ \(0x.*\)//g' | xargs -I {} cp {} ./ -v
```

`ldd` - print shared object dependencies

`sed` - for removing unnecessary string parts

`xargs` - pass each files a input to `cp`

  

## Examples from missing semester Lecture 4

- Remove everything that comes before “Disconnected From”
    
    s-expression, search for that pattern and replace with empty string
    
    ```Python
    cat ssh.log | sed 's/.*Disconnected from//' | less
    ```
    
- sed normally find once and replace once. g modifier
    
    ```Python
    echo 'bbzac' | sed 's/[ab]//g'
    ```
    
- Zero or more of string “ab”, -E is for modern syntax of regular expression. Or it will just match literal parenthesis
    
    ```Python
    echo 'abcaba' | sed -E 's/(ab)*//g'
    ```
    
    - If using old version of regex, escape parenthesis
    
    ```Python
    echo 'abcaba' | sed 's/\(ab\)*//g'
    ```
    
- Capture group in regex for sed
    
    ```Shell
    cat ssh.log | sed -E 's/^.*?Disconnected from (invalid |authenticating )?user (.*) [0-9.]+ port [0-9]+( \[preauth\])?$/\2/' | head -n100
    ```
    
    - `\2` refers to the 2nd capture group
    - If you suffix `+` or `*` with `?` it becomes non-greedy match
    
    Eg: [https://regex101.com/r/qqbZqh/2](https://regex101.com/r/qqbZqh/2)
    
- `wc -l` word count, -l makes it count number of lines
- sort and uniq
    
    ```Shell
    <expression> | sort | uniq -c
    ```
    
    - `-c` count the no. of duplicates
- `awk` is a column-based stream processor.
    
    ```Shell
    <expression> | sort | uniq -c | sort -nk1,1 | tail -n20 | awk '{print $2}' | paste -sd,
    ```
    
    - 2nd sort `-n` numeric sort, `-k` whitespace, `1,1` start at 1st column, stop at 1st column
    - `tail -n20` gives highest 20 counts.
    - `awk` prints 2nd column
    - `paste` pastes text in single line `-s`, with delimiter `-d` ”,”

  

## Missing Semester Lecture 5 Command Line

- Running process in background
    
    ```Shell
    nohup sleep 100 &
    ```
    
    `&` in the end tells bash to run this program in the background
    
    `Ctrl+Z` suspends the job, not quit it
    
- Background Jobs
    
    `jobs` : gives background jobs
    
    this will run background at sequence no 1.
    
    ```Shell
    bg %1
    ```
    
- Killing the job
    
    ```Shell
    kill -STOP %1
    ```
    
    `-STOP` doesn’t kill, just pause it
    
    ```Shell
    kill -HUP %1
    ```
    
    `-HUP` is a hungup signal to the job, it terminates the job
    
- `nohup`
    
    hungup signal will not terminate the job
    
    so `kill -HUP %2` will have no effect on th nohup job
    
    However, `kill -KILL %2` will kill the job no matter what
    

- Example Datasets to play with:
    - [DOB Job Application Filings | NYC Open Data (cityofnewyork.us)](https://data.cityofnewyork.us/Housing-Development/DOB-Job-Application-Filings/ic3t-wcy2)
    - [Databases, Tables & Calculators by Subject (bls.gov)](https://www.bls.gov/data/)