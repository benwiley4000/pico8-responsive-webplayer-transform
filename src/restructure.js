// purge all br elements
var brs = document.querySelectorAll('br');
Array.prototype.forEach.call(brs, function (br) {
  br.parentNode.removeChild(br);
});

// unwrap center elements
var centerElems = document.querySelectorAll('center');
Array.prototype.forEach.call(centerElems, function (elem) {
  var parent = elem.parentNode;
  var children = elem.childNodes;
  for (var i = children.length - 1; i >= 0; i--) {
    parent.insertBefore(children[i], elem);
  }
  parent.removeChild(elem);
});

// add pico8_container class to container element
var container = document.getElementById('canvas').parentNode;
var containerClassName = 'pico8_container';
if (container.classList) {
  container.classList.add(containerClassName);
} else {
  container.className =
    container.className.replace(containerClassName, '') +
    ' ' + containerClassName;
}

// remove element-specific width from container element
container.style.width = '';

// move pico 8 options to new options container element
var options = document.getElementsByClassName('pico8_el');
if (options.length) {
  var optionsContainer = document.createElement('div');
  optionsContainer.className = 'pico8_options';
  container.insertBefore(optionsContainer, options[0]);
  Array.prototype.forEach.call(options, function (option) {
    optionsContainer.appendChild(option);
  });
}
