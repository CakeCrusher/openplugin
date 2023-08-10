(function() {
    // Backup the original fetch function
    const originalFetch = window.fetch;
    let allPlugins = [];
    let totalCount = 0;
    let fetchedCount = 0;

    // Override the fetch function
    window.fetch = async function(...args) {
        const response = await originalFetch.apply(this, args);
        if (args[0].includes('https://chat.openai.com/backend-api/aip/p/approved')) {
            const responseData = await response.clone().json();
            if (responseData && responseData.items) {
                allPlugins = allPlugins.concat(responseData.items);
                console.log(allPlugins); // All plugins have been fetched
                fetchedCount += responseData.items.length;
                if (responseData.count) {
                    totalCount = responseData.count;
                }
                if (fetchedCount < totalCount) {
                    // Simulate a click on the "Next" button to fetch the next page
                    let nextButton = Array.from(document.querySelectorAll('button[role="button"]')).find(btn => btn.textContent.includes('Next') && btn.querySelector('svg'));
                    if (nextButton) {
                        nextButton.click();
                    }
                } else {
                    console.log(allPlugins); // All plugins have been fetched
                }
            }
        }
        return response;
    };

    // Function to click the "All" button
    function clickAllButton() {
        let buttons = document.querySelectorAll('button');
        let allButton = Array.from(buttons).find(btn => btn.textContent.trim() === 'All');
        if (allButton) {
            allButton.click();
        }
    }

    // Execute the clickAllButton function to start the process
    clickAllButton();

})();