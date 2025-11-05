import { useState, useEffect } from 'react';

const pathBackendApi = `http://localhost:8080/api`;

const useFetch = (apiEndpoint) => {
    const [fetchedData, setFetchedData] = useState([]);
    const url = `${pathBackendApi}/${apiEndpoint}`;

    useEffect(() => {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.status);
                }
                return response.json();
            })
            .then(data => {
                setFetchedData(data.data);
            });
    }, [url]);

    return [fetchedData];
};

const CPVCategorieNamesList = () => {
    return useFetch('cpv/categories');
};

export default CPVCategorieNamesList;