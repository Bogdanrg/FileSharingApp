function copy_clipboard(el) {

  // Copy the text inside the text field
  navigator.clipboard.writeText(el.innerHTML);
  let is_copied = document.getElementById("#iscopied");
  console.log(is_copied);
  is_copied.innerHTML = "copied";
  is_copied.style.opacity = "50%";
}
