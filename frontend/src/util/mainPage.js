import JobCard from './jobCard.js';
import FilterSideBar from './sidebar.js';

function MainPage() {
    return (
        <div className='Main'>
          <div className='Side-bar'>
            <FilterSideBar/>
          </div>
          <div className='Card-grid'>
            <div className='Card'>
            <JobCard
              employer="Bouvet"
              title="Frontend Developer"
              location="Sandvika"
              expirationDate="31-12-2025"
              source="LinkedIn"
            />
            </div>
            <div className='Card'>
            <JobCard
              employer="Bouvet"
              title="Frontend Developer"
              location="Sandvika"
              expirationDate="31-12-2025"
              source="LinkedIn"
            />
            </div>
            <div className='Card'>
            <JobCard
              employer="Bouvet"
              title="Frontend Developer"
              location="Sandvika"
              expirationDate="31-12-2025"
              source="LinkedIn"
            />
            </div>
          </div>
        </div>
    );
}

export default MainPage;