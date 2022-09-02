type InitParams = {
  node: HTMLElement | null;
  flags: {
    winWidth: number;
    winHeight: number;
  };
};

export type ElmApp = {};

export declare const Elm: {
  Main: {
    init: (params: InitParams) => ElmApp;
  };
};
