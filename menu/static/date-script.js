// get current date
const currentDate = new Date();

// format the date weekday
const formattedDate = currentDate.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
});

// Set the content of the menu title
document.getElementById('menu-title').textContent = `${formattedDate}`;