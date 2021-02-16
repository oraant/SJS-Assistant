## sjs-daemon 基础的交互操作


>**项目更新后，以下交互相关的内容，全部作废**

| Key \ Modifier | Win -- App         | Shift -- Preset   | Ctrl -- Plus    | Alt -- Minus     |
|:--------------:|--------------------|-------------------|-----------------|------------------|
|    Numpad 1    | Say a dictum       | Start 1st preset  | Plus 1 minutes  | Minus 1 minutes  |
|    Numpad 2    | Talk a joke        | Start 2nd preset  | Plus 2 minutes  | Minus 2 minutes  |
|    Numpad 3    | Read a poem        | Start 3rd preset  | Plus 3 minutes  | Minus 3 minutes  |
|    Numpad 4    | Teach a idiom      | Start 4th preset  | Plus 4 minutes  | Minus 4 minutes  |
|    Numpad 5    | Play a music       | Start 5th preset  | Plus 5 minutes  | Minus 5 minutes  |
|    Numpad 6    | Play a crosstalk   | Start 6th preset  | Plus 6 minutes  | Minus 6 minutes  |
|    Numpad 7    | Tell a story       | Start 7th preset  | Plus 7 minutes  | Minus 7 minutes  |
|    Numpad 8    | Tell me your story | Start 8th preset  | Plus 8 minutes  | Minus 8 minutes  |
|    Numpad 9    | Report system time | Start 9th preset  | Plus 9 minutes  | Minus 9 minutes  |
|  Numpad 0 (10) | Report current job | Start 10th preset | Plus 10 minutes | Minus 10 minutes |


| Key \ Modifier  | Win -- App               | Shift -- Counter           | Ctrl -- Tracer            | Alt -- Bomb             |
|-----------------|--------------------------|----------------------------|---------------------------|-------------------------|
| "." -- Report   | Report last APP & Sound  | Report current Counter     | Report current Tracer     | Report current Bomb     |
| "+" -- Next     | ~~Windows magnifying lens~~ | Switch to next Counter     | Switch to next Tracer     | Switch to next Bomb     |
| "-" -- Previous | ~~Windows magnifying lens~~ | Switch to previous Counter | Switch to previous Tracer | Switch to previous Bomb |
| "*" -- Random   | Run a random APP         | Switch to random Counter   | Switch to random Tracer   | Switch to random Bomb   |
| "/" -- Clear    |                          | Shutdown current Counter   | Shutdown current Tracer   | Deactive current Bomb   |
| "↵" -- Edit     | ~~Windows Can't Register~~ | ~~Edit Preset configuration~~  | Edit Target configuration | Edit Bomb configuration |


>**之前打算要做的交互，也全部作废**

| Key \ Modifier  | Win -- App                  | Shift -- Counter                     | Ctrl -- Tracer                                                          | Alt -- Bomb                                                           | Number 0~9      |
|-----------------|-----------------------------|--------------------------------------|-------------------------------------------------------------------------|-----------------------------------------------------------------------|-----------------|
| "." -- Report   | Report last APP & Sound     | Report current Counter               | Report current Tracer                                                   | Report current Bomb                                                   |                 |
| "+" -- Next     | ~~Windows magnifying lens~~ | Switch to next Counter               | Switch to next Tracer                                                   | Switch to next Bomb                                                   | Plus n minutes  |
| "-" -- Previous | ~~Windows magnifying lens~~ | Switch to previous Counter           | Switch to previous Tracer                                               | Switch to previous Bomb                                               | Minus n minutes |
| "*" -- Random   | Run a random APP            | Switch to random Counter             | Switch to random Tracer                                                 | Switch to random Bomb                                                 | Plus n hours    |
| "/" -- Clear    |                             | Shutdown current Counter             | Shutdown current Tracer                                                 | Deactive current Bomb                                                 | Minus n hours   |
| "↵" -- Edit     | ~~Windows Can't Register~~  | ~~Edit Preset configuration~~        | Edit Target configuration                                               | Edit Bomb configuration                                               |                 |
| Number 0~9      | Open n's APP                | 打开编号为n的预设 一般用来打开计时器 | 选择编号为n的追踪器： 在配置中为常用追踪器编号 若该编号的不活跃，则报告 | 选择编号为n的炸弹： 在配置中为常用的炸弹编号 若该编号的不活跃，则报告 |                 |

> Table edited with [Tables Generator](http://www.tablesgenerator.com/markdown_tables)


## sjs-master 基础的交互操作

| | | | |
|------|----|----|-----|
| Ctrl | -  | +  | ↵   |
| 作用 | +1 | +5 | +10 |


## 如何将py文件设置为开机启动，或者锁定在任务栏

建立一个快捷方式就可以了，只需要注意以下几点：


#### 1，指定起始位置，这里必须填整个项目地址

> 只要在项目路径中，对着要建立快捷方式的文件右键s，系统就会自动填写好正确的起始位置，比如这样：

> E:\WebSite\SJS-Assistant

这是为了防止有些项目里没做路径协调，用相对项目路径引用了一些资源

比如在`SysTrayIcon`相关的代码中，引用了`assets\icon.ico`图标，那么无论是调用哪个路径下的脚本，都会去`当前所处cd路径/assest`路径下找，而非`该脚本的位置/assets`中去找

这点和`import bin`是不同的，导入模块时会根据脚本位置去寻找模块（已验证）


#### 2，指定解释器，这里必须填写虚拟环境中的解释器

> 在cmd或者powershell里怎么写，这里就可以怎么写，无需用引号引起来，比如这样：

> E:\WebSite\SJS-Assistant\venv\Scripts\pythonw.exe E:\WebSite\SJS-Assistant\sjs-daemon.py

如果不指定好解释器，那么使用系统默认版本的python，可能会导致版本不兼容、pip包不齐等问题

如果脚本需要后台运行，那么还要指明是使用`pythonw.exe`，而非`python.exe`


#### 3，将快捷方式放入启动文件夹中，或拖到任务栏上

> 最好做个启动路径的快捷方式，放到方便访问的地方，否则找起来比较麻烦？

> C:\Users\oraant\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

用 `Listary` 搜索 `start menu` 或 `startup` 也可以