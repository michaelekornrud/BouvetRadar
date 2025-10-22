import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders app title (BouvetRadar) as a heading', () => {
  render(<App />);
  const title = screen.getByRole('heading', { name: 'BouvetRadar' });
  expect(title).toBeInTheDocument();
  // Confirm it's an H1 element (semantic)
  expect(title.tagName).toBe('H1');
});

test('renders header logo with correct alt and src', () => {
  render(<App />);
  const logo = screen.getByAltText('Bouvet Logo');
  expect(logo).toBeInTheDocument();
  // check src attribute (exact path used in header.js)
  expect(logo).toHaveAttribute('src', '/Bouvet_Logo_Colossus.svg');
});

test('root elements include expected CSS classes used for layout', () => {
  const { container } = render(<App />);
  // .App should exist
  expect(container.querySelector('.App')).toBeInTheDocument();
  // header wrapper class used in App.js / App.css
  expect(container.querySelector('.App-header')).toBeInTheDocument();
});
