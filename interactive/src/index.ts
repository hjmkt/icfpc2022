import { Elm } from "./Main.elm";

Elm.Main.init({
  node: document.getElementById("container"),
  flags: {
    winWidth: window.innerWidth,
    winHeight: window.innerHeight,
  },
});
