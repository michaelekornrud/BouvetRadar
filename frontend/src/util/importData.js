import { useState, useEffect } from 'react';

const pathBackendApi = `http://localhost:8080/api`;

function CPVCategorieNamesList() {
    const [codes, setCodes] = useState([]);

    useEffect(() => {
        fetch(`${pathBackendApi}/cpv/categories`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.status);
                }
                return response.json();
            })
            .then(data => {
                setCodes(data.data);
            });
    }, [pathBackendApi]);

    return [codes];
}

export default CPVCategorieNamesList;