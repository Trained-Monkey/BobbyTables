import * as React from 'react';
import { addDays } from 'date-fns';
import { useState } from 'react';
import { DateRangePicker } from 'react-date-range';

import 'react-date-range/dist/styles.css'; // main style file
import 'react-date-range/dist/theme/default.css'; // theme css file

export default function TimeQuerier() {

	
	const [state, setState] = useState({
		selection: {
		  startDate: new Date(),
		  endDate: null,
		  key: 'selection'
		},
		compare: {
		  startDate: new Date(),
		  endDate: addDays(new Date(), 3),
		  key: 'compare'
		}
	  });

	const minDate = addDays(new Date(), -30); // TODO: Set this to minimum date of data

	return (
		<>
			<DateRangePicker
				onChange={(item: any) => setState({ ...state, ...item })}
				months={1}
				minDate={minDate}
				maxDate={new Date()}
				direction="vertical"
				scroll={{ enabled: true }}
				ranges={[state.selection, state.compare]}
			/>
		</>
	)
}