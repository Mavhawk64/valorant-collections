import React from "react";
import "./SkinCard.css";

function SkinCard({ skin }) {
    const skinname = skin.melee_name ? skin.melee_name : skin.skin_name + " " + skin.skin_type;
    return (
        <div className="skin-card">
            <h2 className="skin-name">{skinname}</h2>
            <img src={skin.img_link} alt={skinname} className="skin-image" />
        </div>
    );
}

export default SkinCard;
