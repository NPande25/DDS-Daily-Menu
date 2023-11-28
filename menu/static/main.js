// main.js

// Function to fetch and update menu items
async function updateMenu() {
    try {
        const response = await fetch('http://localhost:8000/get_menu');

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        updateHTML(data.lunch, data.dinner);
    } catch (error) {
        console.error('Error fetching menu:', error);
    }
}

// Function to update the HTML content
function updateHTML(lunchItems, dinnerItems) {
    const lunchList = document.getElementById('lunch-items');
    const dinnerList = document.getElementById('dinner-items');

    // Clear existing items
    lunchList.innerHTML = '';
    dinnerList.innerHTML = '';

    // Populate the lists with the new items
    lunchItems.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        lunchList.appendChild(li);
    });

    dinnerItems.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        dinnerList.appendChild(li);
    });
}

// Call the updateMenu function when the page loads
window.onload = updateMenu;
