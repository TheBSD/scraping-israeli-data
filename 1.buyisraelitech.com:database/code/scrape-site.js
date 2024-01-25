// scrapping https://buyisraelitech.com/database
function extractDataFromTable() {
    const dataArray = [];

    // Select all table rows except the header
    const rows = document.querySelectorAll('.notion-collection-table__body tr');

    // Iterate through each row
    rows.forEach(row => {
        const columns = row.querySelectorAll('.notion-collection-table__cell');

        // Extract data from each column
        const name = columns[0].textContent.trim();
        const tags = columns[1].querySelector('.notion-pill').textContent.trim();
        const stage = columns[2].querySelector('.notion-pill').textContent.trim();
        const description = columns[3].textContent.trim();

        // Check if the link exists before trying to access the attribute
        const linkElement = columns[4].querySelector('a');
        const link = linkElement ? linkElement.getAttribute('href') : null;

        // Check if the logo link exists before trying to access the attribute
        const logoElement = columns[5].querySelector('a');
        const logo = logoElement ? logoElement.getAttribute('href') : null;

        const israelRelation = columns[6].querySelector('.notion-pill').textContent.trim();

        // Create an object with extracted data
        const dataObject = {
            Name: name,
            Tags: tags,
            Stage: stage,
            Description: description,
            Link: link,
            Logo: logo,
            IsraelRelation: israelRelation
        };

        // Add the object to the array
        dataArray.push(dataObject);
    });

    return dataArray;
}

// Execute the function and store the result in a variable
const extractedData = extractDataFromTable();

// Log the result to the console
console.log(extractedData);