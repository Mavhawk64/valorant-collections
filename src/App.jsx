import React, { useState, useEffect, useMemo } from "react";
import Papa from "papaparse";
import Fuse from "fuse.js";
import { ENDPOINTS } from "./config/dataEndpoints.js";
import "./App.css";
import SkinCard from "./components/SkinCard.jsx";

// Define the shape of our combined data state
const initialDataState = {
    SKINS: null,
    BANNERS: null,
    SPRAYS: null,
    FLEXES: null,
};

const SKINS_COLS = ["id", "img_link", "edition", "skin_name", "skin_link", "skin_type", "melee_name", "tags"];

function App() {
    const [skins, setSkins] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSkins = async () => {
            setIsLoading(true);
            try {
                Papa.parse(ENDPOINTS.SKINS, {
                    download: true,
                    header: true,
                    skipEmptyLines: true, // Prevents ghost rows from empty spreadsheet cells
                    complete: (results) => {
                        // Filter out any rows that don't at least have a skin_name
                        const validSkins = results.data.filter((row) => row.skin_name);
                        setSkins(validSkins);
                        setIsLoading(false);
                    },
                    error: (err) => {
                        setError("Error parsing CSV: " + err.message);
                        setIsLoading(false);
                    },
                });
            } catch (err) {
                setError("Failed to fetch data. " + err.message);
                setIsLoading(false);
            }
        };

        fetchSkins();
    }, []);

    // Setup Fuse.js for fuzzy searching
    const fuse = useMemo(() => {
        return new Fuse(skins, {
            keys: [
                { name: "skin_name", weight: 0.7 },
                { name: "tags", weight: 0.3 },
            ],
            threshold: 0.3,
        });
    }, [skins]);
    const filteredSkins = useMemo(() => {
        if (!searchTerm) return skins;
        return fuse.search(searchTerm).map((result) => result.item);
    }, [searchTerm, skins, fuse]);

    if (isLoading) return <div className="loading">Loading Skins...</div>;
    if (error) return <div className="error">{error ? error : `bottom text`}</div>;

    return (
        <div className="app-container">
            <div className="header">
                <h1>Valorant Collections Preview</h1>
                {/* Search Bar + Submit Button */}
                <div className="search-bar">
                    <input type="text" placeholder="Search skins..." aria-label="Search skins" className="search-input" onChange={(e) => setSearchTerm(e.target.value)} />
                    <button type="submit" className="search-button">
                        Search
                    </button>
                </div>
            </div>
            <div className="content-wrapper">
                <div className="skins-grid">
                    {filteredSkins.map((skin) => (
                        <SkinCard skin={skin} />
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;
