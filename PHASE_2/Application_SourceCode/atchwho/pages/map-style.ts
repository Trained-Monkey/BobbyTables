import type {FillLayer} from 'react-map-gl';

export const countriesLayer: FillLayer = {
  id: 'country_boundaries',
  type: 'fill',
  'source-layer': 'country_boundaries',
  paint: {
    'fill-outline-color': 'rgba(255,130,0,0.7)',
    'fill-color': 'rgba(255,130,0,0.05)'
  }
};
// Highlighted county polygons
export const highlightLayer: FillLayer = {
  id: 'countries-highlighted',
  type: 'fill',
  source: 'Mapbox Countries v1',
  'source-layer': 'country_boundaries',
  paint: {
    'fill-outline-color': '#484896',
    'fill-color': '#6e599f',
    'fill-opacity': 0.75
  }
};