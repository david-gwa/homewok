
## Simulink basic 

Simulink is the common way to build model based ADAS algorithms, which is the reality in most OEMs. one way to use Simulink model is embedded coder, which transfer Simulink model to C/C++ code, which then is a more common language to other developers, and can build, run, test in Linux x86.

#### S-func 

[Simulink function](https://ww2.mathworks.cn/help/simulink/ug/simulink-functions-overview.html) is a computational unit, with inputs and outputs, can define as:

* Simulink Function block 

* Matlab function

* S-function 

[S-function](https://ww2.mathworks.cn/help/simulink/sfg/what-is-an-s-function.html) is a computer language description of a Simulink block written in MATLAB®, C, C++, or Fortran. for C/C++ types S-func are compiled with *mex*, the s-func is usually used as **dynamic libs** in Matlab/Simulink env.

a simple comparation of Matlab script based S-func vs  C/C++ writen,MeX compiled S-func: 

* for better running performance， using C  Mex S func

* existing C algorithm, called in Simulin, using C Mex S func 

* for embedded coder, using c mex s func 

* for algorithm security, using c mex s func, output as a lib `mexw32/64`

there are four common sub-methods in one S-func: 

* model_initialize()

* model_sampling_timestamps_calc()

* model_step()

* model_terminal()


#### simulink code generator 

there are three ways: simulink coder & embedded coder & simulink V&V 

* simulink coder

which generate a non-optimized code for general hardware env, with input signals and outputs. (grt)


* embedded coder 

which generates optimized code, including variabls naming, structure encaplusing. (ert)


* simulink V&V 


the model can run well in Simulink env, but how to verify the generated code can work as expected in x86 env?  Simulink offer V&V tools. in software standard, embedded coder satisfy Autosar standard, and satisfy IS02626 auto E&E standard as well. 



#### process of code generation 

step1:  `rtwbuild` command to compile model into *.rtw files 

step2:  Traget Language Compiler(TLC) to build  *.rtw files to C/C++ files

during step2, simulink requires system, model TLC configure files. 

step3: generate makefile by Makefile template 


#### structure naming

| models essence  | naming of the struct  |
|--|--|
| extern input | model_U |
| model IO |  model_B |
| extern output |  model_Y |
| configure pars | rtRWork, rtDWork, rtPWork | 
|model pars | model_P |
|model status | model_X|


#### code interface 

```c++ 
model_initialize()
model_step(){
	model_update();
	model_output();
}
```

by default, model_initialize() and model_step() has void parameters and return.



#### integration with external data publisher/receiver

once Simulink code generated, we can feed data into the code through `model_U`, which is basically prepare the data interface from either MCU or data publisher; and the code split out data through `model_Y`, which need to be accepted by a data receiver module. 

Simulink code is in C/C++, once the external data publisher and receiver are both in C++, which means strong type check, we can easily check any un-matching types matching, on the other hand, if the P/R module are in Python, or other weak type check languages, there maybe many mismatching types, which maybe leads to bugs in future. 



#### step rating 

previously, in [mcu know how](https://zjli2013.github.io/2020/08/18/mcu-know-how/) mentioned about **sporadic and aperiodic events**, in `model_step()`,  the sporadic calls/events is running with `overrun` flag, and how to deal with `overrun` is very specially.


#### rt_onestep()


The function rt_OneStep() is always associated with the base rate of the model.  Subrates are managed by the base rate from inside the generated code.

[real-time execution in normal mode](https://in.mathworks.com/help/sldrt/ug/simulink-real-time-normal-mode.html)




## programming in win10 

mostly in Linux, but to integration with Matlab/Simulink, especially during model debugging, there is a need to work in Windows10 env. there are a few setups before a Linux developer getting familiar with Win10. 

* Python conda env 

* GNU C/C++ as plugin in VScode 

* GNU make as plugin in VScode 


#### conda in win10 

[set conda env](https://stackoverflow.com/questions/44597662/conda-command-is-not-recognized-on-windows-10)


by default, conda shell is born from prompt, which is windows shell, like a shit. I'd go to MINGW64, which is a mock-linux shell in windows, and support the same commands as Linux 

* set conda terminal with git mingw64 

```sh
export PATH=$PATH:C/Users/me/Anaconda3:C/Users/me/Anaconda3/Scripts
```

after this setting,  can trigger `conda` from `Git Bash`


* prepare python libs in conda
```sh
conda install numpy
conda install pandas
conda install -c conda-forge asammdf
```


* set python in git terminal 

check [can't run python in git terminal](https://stackoverflow.com/questions/41498580/cant-run-python-in-git-terminal)


#### [c/c++ for vs code](https://code.visualstudio.com/docs/languages/cpp)

* [c/c++ extension in vs code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)

* [install mingw-w64](http://www.mingw-w64.org/doku.php/download)

* [setup win10 subsystem for Linux](https://github.com/acharluk/UsefulStuff/blob/master/windows/setup_wsl.md)

* [using gcc/g++ with  MingGW](https://code.visualstudio.com/docs/cpp/config-mingw)

```sh
C:\Program Files\mingw-w64\x86_64-8.1.0-posix-seh-rt_v6-rev0
```

#### [make for vs code](https://marketplace.visualstudio.com/items?itemName=technosophos.vscode-make)

[on vs code to import makefile projects](https://stackoverflow.com/questions/53674529/is-there-a-way-on-vs-code-to-import-makefile-projects)

[mingw64 ships without make.exe](https://stackoverflow.com/questions/42752721/mingw-64-ships-without-make-exe)





## refer 

[simulink 代码生成](https://www.cnblogs.com/dingdangsunny/p/12269461.html)

[关于模型仿真步长与单片机时间匹配及rt_oneStep函数的应用](https://www.ilovematlab.cn/thread-547265-1-1.html)

[Simulink model/code run in real-time](https://www.cnblogs.com/yunbo/archive/2007/05/31/766981.html)











