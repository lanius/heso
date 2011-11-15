(function () {
  "use strict";
  var getFileLanguage, getIndex, loadScript, setupCodeMirror,
      setUpTextArea, createFileNode,
      textAreas, i, max;

  getFileLanguage = function (fileName) {
    var ext = fileName.split('.').pop(),
        language = "text";
    switch (ext) {
    case 'js':
      language = 'javascript';
      break;
    case 'py':
      language = 'python';
      break;
    case 'rb':
      language = 'ruby';
      break;
    case 'php':
      language = 'php';
      break;
    case 'css':
      language = 'css';
      break;
    case 'html':
      language = 'xml';
      break;
    case 'xml':
      language = 'xml';
      break;
    case 'yml':
      language = 'yaml';
      break;
    case 'yaml':
      language = 'yaml';
      break;
    default:
      break;
    }
    return language;
  };

  getIndex = function (name) {
    return name.match(/(document|filename)\[(\d+)\]/)[2];
  };

  loadScript = function (language, onloadCallback) {
    var url, script;
    if (language !== 'text') {
      url = 'static/lib/codemirror/mode/' + language + '.js';
      script = document.createElement('script');
      script.src = url;
      script.onload = onloadCallback;
      document.body.appendChild(script);
    } else {
      onloadCallback();
    }
  };

  setupCodeMirror = function (textArea, language) {
    var setup = function (textArea, language) {
      var editor, hlLine;
      editor = CodeMirror.fromTextArea(textArea, {
        mode: { name: language },
        theme: "night",
        lineNumbers: true,
        matchBrackets: true,
        onCursorActivity: function () {
          editor.setLineClass(hlLine, null);
          hlLine = editor.setLineClass(editor.getCursor().line, "activeline");
        }
      });
      hlLine = editor.setLineClass(0, "activeline");

      textArea.changeMode = function (language) {
        loadScript(language, function () {
          editor.setOption("mode", language);
        });
      };
    };

    if (language === 'text') {
      setup(textArea, language);
    } else {
      loadScript(language, function () {
        setup(textArea, language);
      });
    }
  };


  setUpTextArea = function (textArea) {
    var fileNameInput = document.getElementsByName("filename[" + getIndex(textArea.name) + "]")[0];

    fileNameInput.onchange = function (event) {
      var fileNameInput, textArea, fileName;
      fileNameInput = event.target;
      textArea = document.getElementsByName("document[" + getIndex(fileNameInput.name) + "]")[0];
      fileName = fileNameInput.value;
      if (!textArea.changeMode) {
        setupCodeMirror(textArea, getFileLanguage(fileName));
      } else {
        textArea.changeMode(getFileLanguage(fileName));
      }
    };

    fileNameInput.onchange({'target': fileNameInput});
  };

  createFileNode = function () {
    var numFiles, fileNode, fileName, textArea;

    numFiles = document.getElementsByClassName("document").length;

    fileNode = document.createElement("div");
    fileNode.className = "well";

    fileName = document.createElement("input");
    fileName.setAttribute("type", "text");
    fileName.setAttribute("name", "filename[" + numFiles + "]");
    fileName.setAttribute("placeholder", "file name");
    fileNode.appendChild(fileName);

    fileNode.appendChild(document.createElement("hr"));

    textArea = document.createElement("textarea");
    textArea.setAttribute("name", "document[" + numFiles + "]");
    textArea.setAttribute("placeholder", "document");
    textArea.className = "document";
    textArea.innerHTML = "\n\n\n\n\n\n\n\n\n\n";
    fileNode.appendChild(textArea);

    // fixme: is there any smart way?
    fileNode.textarea = textArea;

    return fileNode;
  };


  textAreas = document.getElementsByClassName("document");
  for (i = 0, max = textAreas.length; i < max; i += 1) {
    setUpTextArea(textAreas[i]);
  }

  document.getElementById("add").onclick = function () {
    var fileNode = createFileNode();
    document.getElementById("files").appendChild(fileNode);
    setUpTextArea(fileNode.textarea);
    return false;
  };

}());
