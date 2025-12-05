import React, { useState, useEffect } from "react";
import Papa from "papaparse";
import { ENDPOINTS } from "./config/dataEndpoints.js";
import "./App.css";

// Define the shape of our combined data state
const initialDataState = {
    SKINS: null,
    BANNERS: null,
    SPRAYS: null,
    FLEXES: null,
};

// Define the keys we want to extract from the returned row object
const SELECTED_KEYS = ["id", "name", "tags", "img_link"];

function App() {
    // State to hold the data from all four sheets
    const [sheetData, setSheetData] = useState(initialDataState);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAllSheets = async () => {
            setIsLoading(true);
            setError(null);

            // 1. Create a promise for each sheet's parsing operation
            const promises = Object.entries(ENDPOINTS).map(([key, url]) => {
                return new Promise((resolve) => {
                    Papa.parse(url, {
                        download: true,
                        header: true, // Crucial: Treat the first row as headers
                        complete: (results) => {
                            // Extract the first row of data (results.data[0])
                            // and include the sheet key (SKINS, BANNERS, etc.)
                            const rawRow = results.data[0];

                            // 2. Filter the row to only include the selected keys
                            const filteredRow = {};
                            if (rawRow) {
                                for (const k of SELECTED_KEYS) {
                                    // Use 'key' to store the sheet name itself
                                    filteredRow[k] = rawRow[k] || "N/A";
                                }
                                filteredRow.sheet = key;
                            }
                            resolve(filteredRow);
                        },
                        error: (err) => {
                            // Resolve the promise with an error object instead of failing Promise.all
                            resolve({ sheet: key, error: err.message });
                        },
                    });
                });
            });

            try {
                // 3. Wait for all promises (fetch/parse operations) to complete
                const results = await Promise.all(promises);

                // 4. Transform the array of results back into the state object structure
                const newSheetData = results.reduce((acc, rowData) => {
                    if (rowData.sheet) {
                        acc[rowData.sheet] = rowData;
                    }
                    return acc;
                }, initialDataState);

                setSheetData(newSheetData);
            } catch (err) {
                setError("Failed to fetch all data sheets.");
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchAllSheets();
    }, []); // Empty dependency array ensures this runs only once on mount

    if (isLoading) {
        return <div className="loading">Loading data from Google Sheets...</div>;
    }

    if (error) {
        return <div className="error">Error: {error}</div>;
    }

    // Prepare the final array for the table body
    const tableData = Object.values(sheetData).filter((item) => item && !item.error);

    return (
        <div className="app-container">
            <h1>Valorant Collections Preview</h1>

            <table className="data-table">
                <thead>
                    <tr>
                        <th>Sheet</th>
                        {SELECTED_KEYS.map((key) => (
                            <th key={key}>{key.toUpperCase().replace("_", " ")}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {tableData.map((item) => (
                        <tr key={item.sheet}>
                            <td>**{item.sheet}**</td>
                            {/* Map through the selected keys for the cell values */}
                            {SELECTED_KEYS.map((key) => (
                                <td key={key}>
                                    {key === "img_link" && item[key] ? (
                                        <a href={item[key]} target="_blank" rel="noopener noreferrer">
                                            View Image
                                        </a>
                                    ) : (
                                        item[key]
                                    )}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default App;
