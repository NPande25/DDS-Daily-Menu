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

// Function to create a menu item container
function createMenuItem(itemName) {
    const container = document.createElement('div');
    container.classList.add('menu-item');

    const itemNameHeading = document.createElement('h4');
    itemNameHeading.textContent = itemName;

    container.appendChild(itemNameHeading);

    return container;
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
        const listItem = createMenuItem(item);
        lunchList.appendChild(listItem);
    });

    dinnerItems.forEach(item => {
        const listItem = createMenuItem(item);
        dinnerList.appendChild(listItem);
    });
}

// Function to switch between tabs
function showTab(tabName) {
    const tabs = ['ma-thayers', 'collis'];

    tabs.forEach(tab => {
        const tabContent = document.getElementById(`${tab}-content`);
        const button = document.querySelector(`button[data-tab="${tab}"]`);

        if (tab === tabName) {
            tabContent.style.display = 'block';
            button.classList.add('active');
        } else {
            tabContent.style.display = 'none';
            button.classList.remove('active');
        }
    });
}

// Attach the event listeners after the page loads
document.addEventListener('DOMContentLoaded', function () {
    const maThayersTab = document.getElementById('ma-thayers-tab');
    const collisTab = document.getElementById('collis-tab');

    maThayersTab.addEventListener('click', function () {
        showTab('ma-thayers');
    });

    collisTab.addEventListener('click', function () {
        showTab('collis');
    });
});

// Call the updateMenu function when the page loads
window.onload = updateMenu;
