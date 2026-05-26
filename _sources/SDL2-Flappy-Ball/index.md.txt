---
hide-toc: true
orphan: true
---

# Flappy Ball

* [Play the Game (Web Version)](#play-the-game-web-version)
* [Flappy Ball](#gameplay)
* [Development](#development)
  + [I. Windows](#i-windows)
  + [II. Android](#ii-android)
  + [III. Emscripten (Web Assembly)](#iii-emscripten-web-assembly)

This is my first attempt to work with [SDL2](https://en.wikipedia.org/wiki/Simple_DirectMedia_Layer) and game development in general.  
I also experimented with cross-compilation of native apps for Android and Web Assembly.  
SDL Version: [2.30.5](https://github.com/libsdl-org/SDL/releases/tag/release-2.30.5)  


## Demo

Press *SPACEBAR* to start playing.

```{raw} html
    <div class="centered">
        <canvas class="emscripten" id="canvas" oncontextmenu="event.preventDefault()" tabindex=-1></canvas>
    </div>

    <script type='text/javascript'>
      var statusElement = document.getElementById('status');
      var canvasElement = document.getElementById('canvas');

      // As a default initial behavior, pop up an alert when webgl context is lost. To make your
      // application robust, you may want to override this behavior before shipping!
      // See http://www.khronos.org/registry/webgl/specs/latest/1.0/#5.15.2
      canvasElement.addEventListener('webglcontextlost', (e) => {
        alert('WebGL context lost. You will need to reload the page.');
        e.preventDefault();
      }, false);

      var Module = {
        print(...args) {
          console.log(...args);
          // These replacements are necessary if you render to raw HTML
          //text = text.replace(/&/g, "&amp;");
          //text = text.replace(/</g, "&lt;");
          //text = text.replace(/>/g, "&gt;");
          //text = text.replace('\n', '<br>', 'g');
        },
        canvas: canvasElement,
        setStatus(text) {
          if (!Module.setStatus.last) Module.setStatus.last = { time: Date.now(), text: '' };
          if (text === Module.setStatus.last.text) return;
          var m = text.match(/([^(]+)\((\d+(\.\d+)?)\/(\d+)\)/);
          var now = Date.now();
          // if this is a progress update, skip it if too soon
          if (m && now - Module.setStatus.last.time < 30) return;
          Module.setStatus.last.time = now;
          Module.setStatus.last.text = text;
          if (m) {
            text = m[1];
          } else {
          }
          // statusElement.innerHTML = text;
        },
        totalDependencies: 0,
        monitorRunDependencies(left) {
          this.totalDependencies = Math.max(this.totalDependencies, left);
          Module.setStatus(left ? 'Preparing... (' + (this.totalDependencies-left) + '/' + this.totalDependencies + ')' : 'All downloads complete.');
        }
      };
      Module.setStatus('Downloading...');
      window.onerror = (event) => {
        // TODO: do not warn on ok events like simulating an infinite loop or exitStatus
        Module.setStatus('Exception thrown, see JavaScript console');
        Module.setStatus = (text) => {
          if (text) console.error('[post-exception status] ' + text);
        };
      };
    </script>
    <script async type="text/javascript" src="hello-gui-sdl.js"></script>

```

```{include} README.md
:parser: myst_parser.sphinx_
:start-after: <!-- index.md content start -->
:end-before: <!-- index.md content end -->
```
