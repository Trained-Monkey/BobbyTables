import * as React from 'react';
import { addDays } from 'date-fns';
import { useState } from 'react';
import { DateRangePicker } from 'react-date-range';

import 'react-date-range/dist/styles.css'; // main style file
import 'react-date-range/dist/theme/default.css'; // theme css file


export interface Selection {
	startDate: Date,
	endDate: Date | null,
	key: string,
}
export interface SelectionState {
	selections: Selection[],
	setSelections: (selection: Selection[]) => void,
}

export default function TimeQuerier(props: SelectionState) {

	
	
	const minDate = addDays(new Date(), -30); // TODO: Set this to minimum date of data

	return (
		<>
			<DateRangePicker
				onChange={(item: any) => {
					console.log(item);
					props.setSelections([
						{
							...item.selection,
						}
					]);
				}}
				months={1}
				minDate={minDate}
				maxDate={new Date()}
				direction="vertical"
				scroll={{ enabled: true }}
				ranges={props.selections}
			/>
		</>
	)
}