/**
 * by: ohepworthbell
 *  @class
 *  @function Quantity
 *  @param {DOMobject} element to create a quantity wrapper around
 */
 class QuantityInput {
    constructor(self, decreaseText, increaseText) {
      // Create input
      this.input = document.createElement('input');
      this.input.value = 1;
      this.input.type = 'number';
      this.input.name = 'quantity';
      this.input.pattern = '[0-9]+';
  
      // Get text for buttons
      this.decreaseText = decreaseText || 'Decrease quantity';
      this.increaseText = increaseText || 'Increase quantity';
  
      // Button constructor
      function Button(text, className){
        this.button = document.createElement('button');
        this.button.type = 'button';
        this.button.innerHTML = text;
        this.button.title = text;
        this.button.classList.add(className);
  
        return this.button;
      }
  
      // Create buttons
      this.subtract = new Button(this.decreaseText, 'sub');
      this.add = new Button(this.increaseText, 'add');
  
      // Add functionality to buttons
      this.subtract.addEventListener('click', () => this.change_quantity(-1));
      this.add.addEventListener('click', () => this.change_quantity(1));
  
      // Add input and buttons to wrapper
      self.appendChild(this.subtract);
      self.appendChild(this.input);
      self.appendChild(this.add);
      this.input.addEventListener('change', updater)
    }
  
    change_quantity(change) {
      // Get current value
      let quantity = Number(this.input.value);
  
      // Ensure quantity is a valid number
      if (isNaN(quantity)) quantity = 1;
  
      // Change quantity
      quantity += change;
  
      // Ensure quantity is always a number
      quantity = Math.max(quantity, 1);
  
      // Output number
      this.input.value = quantity;
    //   console.log(quantity);
    updater(quantity);
    }
  }
  
  
  // Set up quantity forms
  (function(){
    let quantities = document.querySelectorAll('[data-quantity]');
  
    if (quantities instanceof Node) quantities = [quantities];
    if (quantities instanceof NodeList) quantities = [].slice.call(quantities);
    if (quantities instanceof Array) {
      quantities.forEach(div => (div.quantity = new QuantityInput(div, 'Down', 'Up')));
    }
  })();

// let contador = $('[name="quantity"]')[0];
// contador.addEventListener("change", updateValue);
// function updateValue(e) {
//     // log.textContent = e.target.value;
//     console.log('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
//   }
// function updater(quantity){
//     console.log(quantity);
// }