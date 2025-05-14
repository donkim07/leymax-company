import { Grid } from '@mui/material';
import React from 'react';

/**
 * This file provides wrapper components to fix the TypeScript issues with MUI v5 Grid
 * The issue is that props like xs, sm, md, etc. cause type errors on Grid components
 */

// Wrapper for Grid with item=true
export const Item = (props: any) => <Grid item {...props} />;

// Wrapper for Grid with container=true
export const Container = (props: any) => <Grid container {...props} />;

// Default export of both components
export default { Item, Container }; 