# :globe_with_meridians: Progrez
Heya! I'm presenting you the prettiest progress bar and the typewriter!

![Alt Text](https://s8.gifyu.com/images/1456fd02f849470f8.gif)

## The module includes following features
* **Progrez**
	* own markdown to create a progress bar;
	* async progress;
	* some color animations	such as a rainbow :rainbow: and pulse :comet:;
	* user color sequences.
* **Typewriter**
	* matrix animation (for now supposed to be in exactly one empty line);
	* typing frequency or frame per second (FPS);
	* coloring.

```console
# clone the repo
$ git clone https://github.com/psoglav/progrez.git

# change the working directory to progrez
$ cd progrez

# install
$ python3 setup.py install
```

### This is what planned before next release
- [ ] opportunity to create several progress bars which will be working at the same time;
- [ ] async logging, that is sending messages whilst the progress bar is filling;
- [ ] keywords for each possible color.

### Here is what you need to know before creating the progress bar
There are a few keywords to form the structure of a progress bar.

Keyword | Meaning
------------ | -------------
$progess$ | the bar itself.
$loaderN$ | the loader, appearance of which may be created by a user. *(It may require an index of the loader, identified by the letter N)*
$percentage$ | a percentage of done work.
$paintN$ | starts painting. *(It may require an index of the paint, identified by the letter N)*
$erase$ | stops painting.

> Notice: you are able to rename each of keywords whatever you want using the global variables. For instance: `Progrez.PAINT = 'dye'`


