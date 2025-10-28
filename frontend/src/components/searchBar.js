import { useState } from 'react';

function SearchBar() {
  const [searchTerm, setSearchTerm] = useState('');

  const searchHandler = (e) => {
    if (e.key === 'Enter') {
      const query = e.target.value.trim();
      if (query) {
        console.log('Search for:', query);
      }
    }
  };

  return (
    <input
      type="search"
      placeholder="Søk"
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      onKeyDown={searchHandler}
    />
  );
}

export default SearchBar;
