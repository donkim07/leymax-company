import React, { ReactNode } from 'react';
import { Item } from './MuiGridFix';

// This is a wrapper around our MuiGridFix.Item component for backward compatibility
type GridItemProps = {
  children?: ReactNode;
  [key: string]: any;
};

const GridItem: React.FC<GridItemProps> = ({ children, ...props }) => (
  <Item {...props}>
    {children}
  </Item>
);

export default GridItem; 