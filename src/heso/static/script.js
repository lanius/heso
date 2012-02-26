(function () {
  "use strict";
  
  var STATIC_ROOT = "/static/";
  
  var getFileLanguage = function (fileName) {
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

  var getIndex = function (name) {
    return name.match(/files-(\d+)-(document|filename)/)[1];
  };

  var loadScript = function (language, onloadCallback) {
    var url, script;
    if (language !== 'text') {
      url = STATIC_ROOT + 'lib/codemirror/mode/' + language + '.js';
      script = document.createElement('script');
      script.src = url;
      script.onload = onloadCallback;
      document.body.appendChild(script);
    } else {
      onloadCallback();
    }
  };

  var setupCodeMirror = function (textArea, language) {
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


  var setUpTextArea = function (textArea) {
  
    if (textArea.innerHTML === "") {
      textArea.innerHTML = "\n\n\n\n";
    }

    var fileNameInput = document.getElementsByName("files-" + getIndex(textArea.name) + "-filename")[0];

    fileNameInput.onchange = function (event) {
      var fileNameInput, textArea, fileName;
      fileNameInput = event.target;
      textArea = document.getElementsByName("files-" + getIndex(fileNameInput.name) + "-document")[0];
      fileName = fileNameInput.value;
      if (!textArea.changeMode) {
        setupCodeMirror(textArea, getFileLanguage(fileName));
      } else {
        textArea.changeMode(getFileLanguage(fileName));
      }
    };

    fileNameInput.onchange({'target': fileNameInput});
  };

  var createFileNode = function () {
    var numFiles;
    numFiles = document.getElementsByClassName("document").length;

    var fileNode;
    fileNode = document.createElement("div");
    fileNode.className = "well clearfix";

    var fileName;
    fileName = document.createElement("input");
    fileName.setAttribute("type", "text");
    fileName.setAttribute("id", "files-" + numFiles + "-filename");
    fileName.setAttribute("name", "files-" + numFiles + "-filename");
    fileName.setAttribute("placeholder", "file name");
    fileNode.appendChild(fileName);

    fileNode.appendChild(document.createElement("hr"));

    var textArea;
    textArea = document.createElement("textarea");
    textArea.setAttribute("id", "files-" + numFiles + "-document");
    textArea.setAttribute("name", "files-" + numFiles + "-document");
    textArea.setAttribute("placeholder", "document");
    textArea.setAttribute("rows", "16");
    textArea.setAttribute("cols", "200");
    textArea.className = "document";
    fileNode.appendChild(textArea);

    var removed;
    removed = document.createElement("input");
    removed.type = "hidden";
    removed.value = "false";
    removed.setAttribute("id", "files-" + numFiles + "-removed");
    removed.setAttribute("name", "files-" + numFiles + "-removed");
    removed.className = "removed";
    fileNode.appendChild(removed);

    var removeLink, a;
    removeLink = document.createElement("div");
    a = document.createElement("a");
    a.innerHTML = "remove";
    a.href = "#";
    a.onclick = function () {
      removeFileNode(fileNode);
      return false;
    };
    removeLink.appendChild(a);
    removeLink.className = "remove";
    fileNode.appendChild(removeLink);

    // fixme: is there any smart way?
    fileNode.textarea = textArea;

    return fileNode;
  };

  var removeFileNode = function (fileNode) {
    var removed = fileNode.getElementsByClassName("removed")[0];
    removed.value = true;
    fileNode.style.display = "none";
  };


  var textAreas, fileNodes, i, max;

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

  fileNodes = document.getElementById("files").children;
  for (i = 0, max = fileNodes.length; i < max; i += 1) {
    (function () {
        var fileNode = fileNodes[i];
	    fileNode.getElementsByTagName("a")[0].onclick = function () {
	      removeFileNode(fileNode);
	      return false;
	    };
	}());
  }

}());
