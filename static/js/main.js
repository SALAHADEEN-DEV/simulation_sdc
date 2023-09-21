
const pythonInputCodeEl = document.querySelector("[data-python-input]");
const pythonOutputCodeEl = document.querySelector("[data-python-output]");
// const codeEl = document.querySelector("[data-code]").contentWindow.document;
const runButtonEl = document.querySelector("#run");
const clearButtonEl = document.querySelector("#clear");

const defaultEditorSettings = {
  styleActiveLine: true,
  lineNumbers: true,
  matchBrackets: true,
  tabSize: 2,
  indentUnit: 4,
  theme: "monokai",
  lineWrapping: true,
};

const jsEditor = CodeMirror.fromTextArea(pythonInputCodeEl, {
  ...defaultEditorSettings,
  mode: {
    name: "python",
    version: 3,
    singleLineStringErrors: false
  },
});

const cssEditor = CodeMirror.fromTextArea(pythonOutputCodeEl, {
  ...defaultEditorSettings,
  mode: {
    name: "python",
    version: 3,
    singleLineStringErrors: false
  },
});

// runButtonEl.addEventListener("click", () => {
//   const htmlCode = htmlCodeEl.value;
//   const cssCode = cssCodeEl.value;
//   const jsCode = jsCodeEl.value;

//   codeEl.open();
//   codeEl.write(`<style>${cssCode}</style>`);
//   codeEl.write(htmlCode);
//   codeEl.write(`<script>${jsCode}</script>`);
//   codeEl.close();
// });

// editor.setValue(`sum([1, 2, 3, 4, 5])`);
// output.value = "Initializing...\n";

clearButtonEl.addEventListener("click", () => {
  pythonInputCodeEl.value="";
  pythonOutputCodeEl.value="";
});
