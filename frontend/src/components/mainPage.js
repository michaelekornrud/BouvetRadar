import JobCard from './jobCard.js';
import FilterSideBar from './sidebar.js';
import SearchBar from './searchBar.js';

function MainPage() {
    return (
        <div className='Main'>
          <FilterSideBar/>
          <div className='Card-grid'>
            <JobCard
              employer="Bouvet"
              title="Frontend Developer"
              location="Sandvika"
              expirationDate="31-12-2025"
              source="LinkedIn"
            />
            <JobCard
              employer="Bouvet"
              title="Frontend Developer"
              location="Sandvika"
              expirationDate="31-12-2025"
              source="LinkedIn"
            />
            <JobCard
              employer="Bouvet"
              title="Frontend Developer"
              location="Sandvika"
              expirationDate="31-12-2025"
              source="LinkedIn"
            />
          </div>
          <div className='Search-bar'>
            <SearchBar/>
          </div>
        </div>
    );
}

export default MainPage;