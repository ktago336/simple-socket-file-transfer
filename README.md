# Simple file transfer
File transfering using sockets<br>
<br><b>Use s parameter for the first start</b><hr>
<h2>sync class</h2> <h1>methods</h1>

<h4>checkPath()</h4>checking if existing the path.cfg file (read next)

<h4>getWorkingPath()</h4>returns current path (from path.cfg file) with /files in the end

<h4>getPath()</h4>returns current path (from path.cfg file) without /files in the end

<h4>setPath()</h4>sets and saves current syncronized folder path to the path.cfg file


<h4>firstRun()</h4>sets up folder "files" and "data.cfg" in current directory. "files" - synchronized files, "data.cfg" - stores "files" folder full filepaths as keys of dict and md5 hash as value for changes check, setting up path file to work in different firectories
<h4>createCfg(path)</h4>in current 'path' ("files" folder) walks all directories and saves full file paths in "data.cfg"
<h4>checkSum(path)</h4>compares check sums from "data.cfg" and in 'path', in case of difference of check sums updates this file, and in case if file is not included in "data.cfg" or hashes don't match calls update(path,dirs)
<h4>updateFile(path,dirs)</h4>choose recieve mode for example on server and send mode on your PC, sends file with full name "path", to the IP entered when firstRun() called
