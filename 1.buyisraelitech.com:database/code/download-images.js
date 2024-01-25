// download logos from https://buyisraelitech.com/database
// Function to download logo images with a delay and handle CORS errors
async function downloadLogosWithDelayAndErrorHandling() {
    // Select all table rows except the header
    const rows = document.querySelectorAll('.notion-collection-table__body tr');

    // Array to store URLs with CORS issues
    const corsErrorUrls = [];

    // Iterate through each row with a delay
    for (const [index, row] of rows.entries()) {
        const columns = row.querySelectorAll('.notion-collection-table__cell');

        // Extract data from each column
        const name = columns[0].textContent.trim();

        // Check if the logo link exists before trying to download
        const logoElement = columns[5].querySelector('a');
        if (logoElement) {
            const logoUrl = logoElement.getAttribute('href');

            try {
                // Fetch the logo image data
                const response = await fetch(logoUrl);
                const blob = await response.blob();

                // Create a data URL for the image
                const dataUrl = URL.createObjectURL(blob);

                // Create a link element to simulate a click for download
                const link = document.createElement('a');
                link.href = dataUrl;

                // Set the download attribute with the company name as the file name
                link.download = `${name}_logo.svg`;

                // Append the link to the document
                document.body.appendChild(link);

                // Simulate a click to trigger the download
                link.click();

                // Remove the link from the document after a delay
                setTimeout(() => {
                    document.body.removeChild(link);
                }, 1000); // Adjust the delay as needed (1000 milliseconds = 1 second)
            } catch (error) {
                // Handle CORS errors
                console.error(`CORS error for ${logoUrl}:`, error);
                corsErrorUrls.push(logoUrl);
            }
        }

        // Introduce a delay between each download (adjust as needed)
        await new Promise(resolve => setTimeout(resolve, 2000)); // 2000 milliseconds = 2 seconds
    }

    // Log URLs with CORS issues
    console.log('URLs with CORS issues:', corsErrorUrls);
}

// Execute the function to download logos with a delay and handle CORS errors
downloadLogosWithDelayAndErrorHandling();