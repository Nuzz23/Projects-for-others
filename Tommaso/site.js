// Function to get data from localStorage
function getLocalStorage() {
    // function gets the local storage items associated to the user
    // or else an empty list
    return JSON.parse(localStorage.getItem('userItems')) || [];
}

// Function to set data to localStorage
function setLocalStorage(data){
    // Saves item just added to local storage
    localStorage.setItem('userItems', JSON.stringify(data));
}

// Function to render items from localStorage
function renderItems() {
    // gets the currently saved items
    const items = getLocalStorage();
    //gets the id of the html element where the list should be outputted to
    var outputDiv = document.getElementById('list-output');
    //Clears the list
    outputDiv.innerHTML = "";
    // for each item in the list
    items.forEach(function(item, index) {
        // the new item  is created with tag article 
        var newItem = document.createElement('article');
        // Class = "list-item" which is used for css purposes
        newItem.classList.add('list-item');
        // finally, the element is added to the just created article
        // the text is h5 and occupies the first column 
        // whilst the other three smaller columns are occupied by the three icons
        newItem.innerHTML = `
            <h5>${item.text}</h5>
            <div class="icon"><img src="img/check.png"  alt="check"  class="check img"></div>
            <div class="icon"><img src="img/modify.png" alt="modify" class="modify img"></div>
            <div class="icon"><img src="img/delete.png" alt="delete" class="delete img"></div>
        `;
        // the item is attached to the item list
        outputDiv.appendChild(newItem);

        // Add event listener for the check icon
        // selects the element icon and then the text for the if and the change of style
        var checkIcon = newItem.querySelector('.check');
        var itemText = newItem.querySelector('h5');
        // if item is completed (checked) then change style
        if (item.completed) {
            itemText.style.color = 'grey';
            itemText.style.textDecoration = 'line-through';
        }
        // for every click on the icon the state is changed to reflect
        // the possibility of double clicking 
        checkIcon.addEventListener('click', function() {
            item.completed = !item.completed;
            // The modification is then stored and items are rendered
            setLocalStorage(items);
            renderItems();
        });

        // Add event listener for the modify icon
        // the icon is selected
        var modifyIcon = newItem.querySelector('.modify');
        // the item text is copied and pasted on the input group
        // then the item is deleted and the changed are done also
        // in the local file storage 
        modifyIcon.addEventListener('click', function() {
            document.getElementById('name-input').value = item.text;
            items.splice(index, 1);
            setLocalStorage(items);
            renderItems();
        });

        // Add event listener for the delete icon
        // Behaves similarly to the modify command
        // but without copying and pasting the text in the input group
        var deleteIcon = newItem.querySelector('.delete');
        deleteIcon.addEventListener('click', function() {
            items.splice(index, 1);
            setLocalStorage(items);
            renderItems();
        });
    });
}

// This function works on the button add item associated to the input group
document.getElementById('add-btn').addEventListener('click', function() {
    // the value inside the input group is collected (using his id)
    // the value is then trimmed for spaces at the beginning/end
    var input = document.getElementById('name-input').value.trim();
    // if the text inputted is not the empty string
    if (input !== "") {
        // then get the local storage items (the items already saved)
        const items = getLocalStorage();
        // Push the new one to it and set it's status as not completed
        items.push({ text: input, completed: false });
        // save items and render them on screen
        setLocalStorage(items);
        renderItems();
        // clear the input field from the text previously written
        document.getElementById('name-input').value = "";  
    }
});

// this function regard the use of the clear button
// once pressed the local storage is emptied 
// then the items present (ideally none) are rendered 
// which results in an empty list of items
// Also clears the item input text
document.getElementById('clear-btn').addEventListener('click', function() {
    localStorage.removeItem('userItems');
    renderItems();
    document.getElementById('name-input').value="";
});

// Load items on page load (as soon as the DOM is loaded)
document.addEventListener('DOMContentLoaded', renderItems);
