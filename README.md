# :globe_with_meridians: Progrez
Heya! Here are the beautiful python progress bar and typewriter!

## The module includes following features
* **Progrez**
	* own markdown to create a progress bar;
	* async progress;
	* some color animations	such as a rainbow :rainbow: and pulse :comet:;
	* user color sequences.
* **Typewriter**
	* matrix animation (supposed to be in exactly one empty line);
	* typing frequency or frame per second (FPS);
	* coloring.

### This is what's planned before next release
- [ ] opportunity to create several progress bars which will be working at the same time;
- [ ] async logging, that is sending messages whilst the progress bar filling;
- [ ] keywords for each possible color.

### Here is what you need to know before creating the progress bar
There are a few keywords to form the structure of a progress bar.

Keyword | Meaning
------------ | -------------
$progess$ | the bar itself.
$loaderN$ | a loader whose appearance may be created by an user. *(It may require an index of the loader, identified by the letter N)*
$percentage$ | a percentage of done work.
$paintN$ | an user paint. *(It may require an index of the paint, identified by the letter N)*

> Notice: you are able to rename each of keywords whatever you want using the global variables. For instance: `Progrez.PAINT = 'dye'`


