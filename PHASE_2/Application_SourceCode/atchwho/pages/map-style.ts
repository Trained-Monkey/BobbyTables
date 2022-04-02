import type {FillLayer} from 'react-map-gl';

export const countriesLayer: FillLayer = {
  id: 'country_boundaries',
  type: 'fill',
  'source-layer': 'country_boundaries',
  filter: [
    'all',
    ['match', ['get', 'worldview'], ['all', 'US'], true, false],
    ["!=", "true", ["get", "disputed"]],
  ],
  paint: {
    'fill-outline-color': 'rgba(255,130,0,0.7)',
    'fill-color': 'rgba(255,130,0,0.05)'
  }
};

// Highlighted county polygons
export const highlightLayer: FillLayer = {
	id: 'country_highlighted',
	type: 'fill',
	'source-layer': 'country_boundaries',
	filter: [
	  'all',
	  ['match', ['get', 'worldview'], ['all', 'US'], true, false],
	  ["!=", "true", ["get", "disputed"]],
	],
	paint: {
		'fill-color': 'rgba(255,130,0,1)',
	}
}

